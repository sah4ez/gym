import gym
import examples.skier.agent as agent
from examples.skier.coordinate import coordinates
from gym import wrappers

if __name__ == '__main__':

    env = gym.make('Skiing-v0')
    out = '/tmp/skiing'
    env = wrappers.Monitor(env, directory=out, force=True)
    env.seed(0)

    # ag = agents()
    action = 1

    rewards = []
    reward = 0
    done = False

    count = 0
    for i in range(2):
        observation = env.reset()
        ag = agent.agents()

        # for t in range(500):
        while True:
            env.render()
            action = ag.act(observation)
            # action = env.action_space.sample()
            if isinstance(action, int):
                observation, reward, done, info = env.step(action)

            print("# ", str(count),
                  "P ", str(coordinates(ag.pos_skier[0], ag.pos_skier[1])),
                  " :: F ", str(coordinates(ag.pos_flags[0], ag.pos_flags[1])),
                  # " :: T ", str(coordinates(ag.pos_trees[0], ag.pos_trees[1])),
                  # " :: D ", str(coordinates(ag.pos_dirties[0], ag.pos_dirties[1])),
                  " :: A ", str(ag.angle),
                  " :: REWARD ", str(reward),
                  " :: ACTION ", str(action),
                  " :: DELTA {:.2f}".format(ag.last_delta),
                  " :: LENGTH {:.2f}".format(ag.last_length),
                  " :: VELOCITY {:.2f}".format(ag.current_velocity)
                  )
            count += 1

            print("\n========================================\n")
            if done:
                print(reward)
                rewards.append(reward)
                # print('Episode finished after {} timesteps'.format(t + 1))
                break

    env.close()

    print(rewards)

    gym.upload(out)
