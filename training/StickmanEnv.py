import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import random


class Platform:
    def __init__(self, x, y, width=100, height=20):
        self.rect = pygame.Rect(x, y, width, height)


class StickmanEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode=None):
        super().__init__()

        # World size
        self.width = 1000
        self.height = 500

        # Physical parameters
        self.gravity = 0.5
        self.jump_strength = -10
        self.max_speed = 10
        self.platform_count_range = (6, 8)
        self.platform_spacing = (100, 180)

        # Observations = position/speed + 8 platforms max (dx, dy)
        self.max_platforms = 8
        obs_dim = 4 + 2 * self.max_platforms
        self.observation_space = spaces.Box(
            low=np.full(obs_dim, -1000.0, dtype=np.float32),
            high=np.full(obs_dim, 1000.0, dtype=np.float32),
            dtype=np.float32
        )

        # Action space : nothing, left, right, jump
        self.action_space = spaces.Discrete(4)

        self.render_mode = render_mode
        if render_mode == "human":
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.clock = pygame.time.Clock()

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.pos = np.array([100.0, 400.0])
        self.vel = np.array([0.0, 0.0])
        self.is_grounded = False
        self.done = False

        # Génération des plateformes
        self.platforms = []
        num_platforms = random.randint(*self.platform_count_range)

        # Plateforme de départ
        start_x, start_y = 100, 460
        self.platforms.append(Platform(start_x, start_y, width=self.width, height=20))  # sol

        x, y = 200, 400
        for _ in range(num_platforms):
            dx = random.randint(*self.platform_spacing)
            dy = random.randint(-100, 100)
            x += dx
            y = np.clip(y + dy, 380, 440)
            self.platforms.append(Platform(x, y))

        self.goal_x = x  # objectif final

        return self._get_obs(), {}

    def _get_obs(self):
        obs = [self.pos[0], self.pos[1], self.vel[0], self.vel[1]]
        # Every platform except ground for now (will be changed when the platforms will be rendered correctly as a reel platform game)
        for plat in self.platforms[1:]:
            dx = plat.rect.centerx - self.pos[0]
            dy = plat.rect.centery - self.pos[1]
            obs.extend([dx, dy])

        # Adding padding if there's less than 8 platforms (not really useful since the main platform does the screen width)
        while len(obs) < 4 + 2 * self.max_platforms:
            obs.extend([0.0, 0.0])

        return np.array(obs, dtype=np.float32)

    def step(self, action):
        reward = 0

        # Actions
        if action == 1:
            self.vel[0] = -3
        elif action == 2:
            self.vel[0] = 3
        else:
            self.vel[0] = 0

        if action == 3 and self.is_grounded:
            self.vel[1] = self.jump_strength

        # Physic
        self.vel[1] += self.gravity
        self.vel[1] = min(self.vel[1], self.max_speed)
        self.pos += self.vel

        # Collisions
        self.is_grounded = False
        for plat in self.platforms:
            if (
                self.pos[1] + 60 >= plat.rect.top and
                self.pos[1] + 60 <= plat.rect.top + 10 and
                plat.rect.left - 40 < self.pos[0] < plat.rect.right
            ):
                self.pos[1] = plat.rect.top - 60
                self.vel[1] = 0
                self.is_grounded = True

        # Limits
        self.pos[0] = np.clip(self.pos[0], 0, self.width)
        if self.pos[1] > self.height:
            self.done = True
            reward -= 10  # mort

        # Reward
        reward += (self.pos[0] / self.goal_x)  # move forward = reward
        if self.pos[0] >= self.goal_x:
            reward += 10
            self.done = True

        return self._get_obs(), reward, self.done, False, {}

    def render(self):
        if self.render_mode != "human":
            return

        self.screen.fill((255, 255, 255))

        # Plateformes
        for plat in self.platforms:
            pygame.draw.rect(self.screen, (0, 200, 0), plat.rect)

        # Stickman
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(*self.pos, 40, 60))

        pygame.display.flip()
        self.clock.tick(self.metadata["render_fps"])

    def close(self):
        if self.render_mode == "human":
            pygame.quit()
