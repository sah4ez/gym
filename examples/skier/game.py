import gym
import examples.skier.agent as agent
from examples.skier.coordinate import coordinates

if __name__ == '__main__':

    env = gym.make('Skiing-v0')
    out = '/tmp/skiing'
    # env = wrappers.Monitor(env, out)

    # ag = agents()
    action = 1

    count = 0
    for i in range(20):
        observation = env.reset()
        ag = agent.agents()

        for t in range(1500):
            env.render()
            # print(observation)
            action = ag.act(observation)
            # action = env.action_space.sample()
            observation, reward, done, info = env.step(action)

            print("# ", str(count),
                  "P ", str(coordinates(ag.pos_skier[0], ag.pos_skier[1])),
                  " :: F ", str(coordinates(ag.pos_flags[0], ag.pos_flags[1])),
                  " :: T ", str(coordinates(ag.pos_trees[0], ag.pos_trees[1])),
                  " :: D ", str(coordinates(ag.pos_dirties[0], ag.pos_dirties[1])),
                  " :: A ", str(ag.angle),
                  " :: ACTION ", str(action)
                  )
            count += 1

            print("\n========================================\n")
            if done:
                print(reward)
                print('Episode finished after {} timesteps'.format(t + 1))
                break
