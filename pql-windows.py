import numpy as np
import matplotlib.pyplot as plt

import gym
import rubiks_cube_gym # noqa

import warnings
from datetime import datetime
import argparse
import pickle
import gc
from multiprocessing import shared_memory, Process
from multiprocessing import cpu_count, current_process

plt.style.use('seaborn-dark')
warnings.filterwarnings("ignore")


def create_qtable(input_qt=None):
    if input_qt is None:
        q_table_init = np.full([env.observation_space.n, env.action_space.n], -100, dtype=np.float32)
    else:
        with open(input_qt, "rb") as f:
            q_table_init = pickle.load(f)

    shm = shared_memory.SharedMemory(create=True, size=q_table_init.nbytes)
    q_table = np.ndarray(q_table_init.shape, dtype=np.float32, buffer=shm.buf)
    q_table[:] = q_table_init[:]
    return shm, q_table


def train(shr_name, episodes_per_process, render_enable, env, op):
    EPISODES = episodes_per_process
    GROUP_SIZE = 10000
    LEARNING_RATE = 0.1
    DISCOUNT = 0.9
    EPSILON = 1.0
    START_EPSILON_DECAYING = 1
    END_EPSILON_DECAYING = EPISODES * 0.9
    EPSILON_DECAY = EPSILON / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

    episode_rewards = []
    episode_success = []
    process_no = current_process().name
    existing_shm = shared_memory.SharedMemory(name=shr_name)
    q_table = np.ndarray((env.observation_space.n, env.action_space.n), dtype=np.float32, buffer=existing_shm.buf)

    for episode in range(EPISODES):
        if episode % GROUP_SIZE == 0:
            if current_process().name == "Process-1":
                print(f"Process:{process_no}, Episode number:{episode}/{EPISODES} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Epsilon:{EPSILON:.4f} {GROUP_SIZE} reward mean: {np.mean(episode_rewards[-GROUP_SIZE:]):.4f} "
                      f"{GROUP_SIZE} success mean: {np.mean(episode_success[-GROUP_SIZE:]):.4f}")
                print()
                render = True
            else:
                render = False

        state = env.reset()

        episode_reward = 0
        success = 0
        done = False

        while not done:
            if np.random.randn() > EPSILON:
                action = np.argmax(q_table[state])
            else:
                action = np.random.randint(0, env.action_space.n)

            new_state, reward, done, info = env.step(action)

            max_future_q = np.max(q_table[new_state])
            current_q = q_table[state][action]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[state][action] = new_q

            episode_reward += reward

            if render and render_enable:
                env.render()

            if reward >= 60:
                success = 100

            state = new_state

        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            EPSILON = max(EPSILON - EPSILON_DECAY, 0)

        episode_rewards.append(episode_reward)
        episode_success.append(success)

    existing_shm.close()
    plot(GROUP_SIZE, episode_rewards, episode_success, op)


def plot(GROUP_SIZE, episode_rewards, episode_success, op):
    moving_avg = np.convolve(episode_rewards, np.ones((GROUP_SIZE,)) / GROUP_SIZE, mode="valid")
    moving_success = np.convolve(episode_success, np.ones((GROUP_SIZE,)) / GROUP_SIZE, mode="valid")

    with open(op + "_" + current_process().name + "_stats" + ".pickle", "wb") as f:
        stats = {"reward": episode_rewards, "success": episode_success}
        pickle.dump(stats, f)

    fig, ax = plt.subplots()
    ax.plot([i for i in range(len(moving_avg))], moving_avg, color='tab:blue', linewidth=2)
    ax.set_ylabel(f"reward {GROUP_SIZE} moving average", color='tab:blue')
    ax.set_xlabel("episode #")

    ax2 = ax.twinx()
    ax2.plot([i for i in range(len(moving_success))], moving_success, color='tab:red', linewidth=2)
    ax2.set_ylabel(f"success {GROUP_SIZE} moving average", color='tab:red')

    fig.savefig(op + "_" + current_process().name + ".png", format='png', dpi=100, bbox_inches='tight')


def close():
    env.close()
    gc.collect()


def save_qtable(q_table):
    with open(op + "_qtable" + ".pickle", "wb") as f:
        pickle.dump(q_table, f)


if __name__ == '__main__':
    if current_process().name == "MainProcess":

        parser = argparse.ArgumentParser(description='Validate a q_table against scrambles from WCA competitions')
        parser.add_argument('-op', '--output', help="Output file name")
        parser.add_argument('-e', '--env', required=True, help="Environment name")
        parser.add_argument('-s', '--size', type=int, default=100000, help="Number of episodes")
        parser.add_argument('-ip', '--input', default=None, help="Input Q Table name")
        parser.add_argument('-r', '--render', default=False, type=bool, help="Render once every GROUP_SIZE")

        args = parser.parse_args()
        episodes_per_process = args.size // cpu_count()
        render_enable = args.render
        if args.output is None:
            op = f"{args.env}_{args.size}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        else:
            op = args.output

        env = gym.make(args.env)

        t = datetime.now()

        print("Creating shared block")
        shr, q_table = create_qtable(input_qt=args.input)

        processes = []
        for i in range(cpu_count()):
            _process = Process(target=train, args=(shr.name, episodes_per_process, render_enable, env, op))  # passing variables explicitly to support Windows
            processes.append(_process)
            _process.start()

        for _process in processes:
            _process.join()

        print(f"Training time: {datetime.now() - t}")

        close()
        save_qtable(q_table)

        shr.close()
        shr.unlink()
