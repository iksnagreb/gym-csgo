# Gym environment registration
from gym.envs.registration import register

# Register the csgo environment
register(id='csgo-v0', entry_point='gym_csgo.envs:CSGOEnv')

# Register the csgo casual mode environment
register(id='csgo_casual-v0', entry_point='gym_csgo.envs:CSGOCasualEnv')

# Register the csgo deathmatch mode environment
register(id='csgo_dm-v0', entry_point='gym_csgo.envs:CSGODeathmatchEnv')
