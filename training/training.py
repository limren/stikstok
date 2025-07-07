from stable_baselines3 import PPO
from StickmanEnv import StickmanEnv

env = StickmanEnv(render_mode=None)
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100_000)
model.save("ppo_stickman_jump")
