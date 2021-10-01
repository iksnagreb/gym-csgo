# OpenAI gym environments
import gym
# Numpy arrays
import numpy as np


# Enum (from string) observation/action space
class Enum(gym.spaces.Discrete):
    # Constructs an Enum space from selection of values
    def __init__(self, *values: str, seed=None):
        # Construct Discrete space super class of number of values
        super().__init__(len(values), seed=seed)
        # Store names of enum values
        self.values = np.array(sorted(values))

    # Samples from enum values
    def sample(self):
        # Use Discrete baseclass sample to select from enum values
        return self.values[super().sample()]

    # Checks whether Enum space contains a value
    def contains(self, x):
        # Test whether item in enum values (list)
        return x in self.values

    # Produces string representation of the enum space
    def __repr__(self):
        return "Enum(" + ','.join(self.values) + ")"

    # Compares to other space (Enum)
    def __eq__(self, other):
        return isinstance(other, Enum) and self.values == other.values
