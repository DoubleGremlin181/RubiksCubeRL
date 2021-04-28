import numpy as np

import gym
import rubiks_cube_gym # noqa

import pickle
import argparse


def solve_scramble(scramble):
    state = env.reset(scramble=scramble)
    number_of_moves = 0
    episode_reward = 0
    success = 0
    done = False

    if render:
        env.render()

    while not done:
        action = np.argmax(q_table[state])
        new_state, reward, done, info = env.step(action)
        episode_reward += reward

        if render:
            env.render(render_time=500)
        print(action, end=" ")

        if reward >= 60:
            success = 100

        state = new_state
        number_of_moves += 1

    print()
    return episode_reward, success, number_of_moves


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate a q_table against scrambles from WCA competitions')
    parser.add_argument('-q', '--q_table', required=True, help="Q Table name")
    parser.add_argument('-e', '--env', required=True, help="Environment name")
    parser.add_argument('-s', '--scramble', required=True, help="Scramble to solve")
    parser.add_argument('-r', '--render', type=bool, default=False, help="Render the solution")

    args = parser.parse_args()

    env = gym.make(args.env)

    with open(args.q_table, "rb") as f:
        q_table = pickle.load(f)

    render = args.render

    episode_reward, success, number_of_moves = solve_scramble(args.scramble)

    print("----RESULTS----")
    print(f"Reward: {episode_reward}")
    print(f"Success: {success}")
    print(f"Number of moves: {number_of_moves}")

