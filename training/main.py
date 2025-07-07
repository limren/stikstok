from stable_baselines3 import PPO
from StickmanEnv import StickmanEnv

env = StickmanEnv(render_mode="human")
model = PPO.load("ppo_stickman_jump")

obs, _ = env.reset()
done = False

while not done:
    action, _ = model.predict(obs)
    obs, reward, done, _, _ = env.step(action)
    env.render()

env.close()
