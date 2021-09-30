# OpenAI gym environments
import gym


# Constructs a Counter Strike action space
def make_act_space():
    # Return action space dictionary
    return gym.spaces.Dict({
        'forward': gym.spaces.Discrete(2),
        'back': gym.spaces.Discrete(2),
        'left': gym.spaces.Discrete(2),
        'right': gym.spaces.Discrete(2),
        'walk': gym.spaces.Discrete(2),
        'jump': gym.spaces.Discrete(2),
        'duck': gym.spaces.Discrete(2),
        'fire': gym.spaces.Discrete(2),
        'special': gym.spaces.Discrete(2),
        'reload': gym.spaces.Discrete(2),
        'drop': gym.spaces.Discrete(2),
        'use': gym.spaces.Discrete(2),
        'switch': gym.spaces.Discrete(2),
        'healthshot': gym.spaces.Discrete(2),
        'equip': gym.spaces.Discrete(10),
        'camera': gym.spaces.Box(low=-540.0, high=540.0, shape=(2,))
    })


# Creates a noop (do nothing) action
def make_noop():
    # Return dictionary with all action set to 0 (False)
    return {
        # Do not move
        'forward': 0, 'back': 0, 'left': 0, 'right': 0,
        # No sneaking, hiding, ...
        'walk': 0, 'jump': 0, 'duck': 0,
        # No interacting
        'fire': 0, 'special': 0, 'reload': 0, 'drop': 0, 'use': 0,
        # No weapon change
        'switch': 0, 'healthshot': 0, 'equip': None,
        # Do not look around
        'camera': [0, 0]
    }
