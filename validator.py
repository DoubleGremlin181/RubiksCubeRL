import numpy as np
import pandas as pd

import gym
import rubiks_cube_gym # noqa

from p_tqdm import p_umap
import pickle
import argparse


def eval_scramble(scramble):
    state = env.reset(scramble=scramble)
    number_of_moves = 0
    episode_reward = 0
    success = 0
    done = False

    while not done:
        action = np.argmax(q_table[state])
        new_state, reward, done, info = env.step(action)
        episode_reward += reward

        if reward >= 60:
            success = 100

        state = new_state
        number_of_moves += 1

    return episode_reward, success, number_of_moves


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate a q_table against scrambles from WCA competitions')
    parser.add_argument('-q', '--q_table', required=True, help="Q Table name")
    parser.add_argument('-p', '--puzzle', required=True, help="WCA event ID")
    parser.add_argument('-e', '--env', required=True, help="Environment name")
    parser.add_argument('-s', '--size', type=int, default=10000, help="Size of validation set")
    parser.add_argument('-t', '--track', type=bool, default=True, help="Write the stats to a CSV")

    args = parser.parse_args()

    env = gym.make(args.env)

    df = pd.read_csv('WCA_scrambles_clean.csv')
    df = df[df['eventId'] == args.puzzle]

    if df.shape[0] < args.size:
        print("Number of scrambles available is  less than the size specified, setting size to be the maximum possible")
        args.size = df.shape[0]

    df = df.sample(n=args.size)

    with open(args.q_table, "rb") as f:
        q_table = pickle.load(f)

    results = p_umap(eval_scramble, df.scramble.to_list())

    episode_rewards = [result[0] for result in results]
    episode_success = [result[1] for result in results]
    episode_number_of_moves = [result[2] for result in results]

    reward_mean = np.mean(episode_rewards)
    success_mean = np.mean(episode_success)
    number_of_moves_mean = np.mean(episode_number_of_moves)

    if args.track:
        df = pd.DataFrame([[args.q_table, args.puzzle, args.size, reward_mean, success_mean, number_of_moves_mean]],
                           columns=["Table", "Puzzle", "Size of validation set", "Average reward", "Success rate", "Average number of moves"])
        with open("tracker.csv", 'a') as f:
            df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

    print("----RESULTS----")
    print(f"Reward mean: {reward_mean}")
    print(f"Success mean: {success_mean}")
    print(f"Number of moves mean: {number_of_moves_mean}")

