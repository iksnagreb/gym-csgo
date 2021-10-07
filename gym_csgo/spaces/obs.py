# OpenAI gym environments
import gym
# Numpy arrays
import numpy as np
# Game weapon specifications
from gym_csgo.specs.weapon import WEAPON_NAMES, WEAPON_TYPES, NUM_WEAPON_SLOTS
# Enumeration observation space
from .enum import Enum


# Constructs a Counter Strike weapon observation space
def make_weapon_obs_space():
    # Observation space base components
    from gym.spaces import Box
    # Return observation space dictionary
    return gym.spaces.Dict({
        # Name of the weapon
        'name': Enum(*WEAPON_NAMES, 'none'),
        # Type of the weapon
        'type': Enum(*WEAPON_TYPES, 'none'),
        # State of weapon
        'state': Enum('active', 'holstered', 'reloading', 'none'),
        # Current amount of ammo in the clip
        'ammo_clip': Box(low=0, high=np.inf, shape=(1,)),
        # Maximum amount of ammo the clip for the weapon can hold
        'ammo_clip_max': Box(low=0, high=np.inf, shape=(1,)),
        # Amount of extra (reserve) ammo available for the weapon
        'ammo_reserve': Box(low=0, high=np.inf, shape=(1,))
    })


# Constructs a Counter Strike weapon observation space
def make_obs_space(pov_shape=(640, 480, 3)):
    # Observation space base components
    from gym.spaces import Box, Discrete
    # Get the weapon observation space
    weapon  = make_weapon_obs_space()
    # Return observation space dictionary
    return gym.spaces.Dict({
        # Observation image
        'pov': Box(low=0, high=255, shape=pov_shape, dtype=np.uint8),
        # Player state
        'health': Box(low=0, high=np.inf, shape=(1,)),
        'armor': Box(low=0, high=np.inf, shape=(1,)),
        'helmet': Discrete(2),
        'flashed': Box(low=0, high=255, shape=(1,), dtype=np.uint8),
        'smoked': Box(low=0, high=255, shape=(1,), dtype=np.uint8),
        'burning': Box(low=0, high=255, shape=(1,), dtype=np.uint8),
        'money': Box(low=0, high=np.inf, shape=(1,)),
        'value': Box(low=0, high=np.inf, shape=(1,)),
        # Player stats
        'kills': Box(low=0, high=np.inf, shape=(1,)),
        'assists': Box(low=0, high=np.inf, shape=(1,)),
        'deaths': Box(low=0, high=np.inf, shape=(1,)),
        'mvps': Box(low=0, high=np.inf, shape=(1,)),
        'score': Box(low=0, high=np.inf, shape=(1,)),
        # The player's team
        'team': Enum('CT', 'T', 'none'),
        # The player's active weapon
        'weapon_active': weapon,
        # All the player's weapons
        **{f'weapon_{i}': weapon for i in range(NUM_WEAPON_SLOTS)},
    })
