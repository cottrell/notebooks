import gym
import gym.spaces

def run():
    env = gym.make('CartPole-v0')
    total_reward = 0.0
    total_steps = 0
    obs = env.reset()
    while True:
        action = env.action_space.sample()
        obs, reward, done, _ = env.step(action)
        total_reward += reward
        total_steps += 1
        if done:
            break
