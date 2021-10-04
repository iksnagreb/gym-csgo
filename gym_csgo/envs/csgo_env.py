# Sleeping
from time import sleep
# OpenAI gym environments
import gym
# Show image using OpenCV
import cv2
# Virtual display server
from gym_csgo.glue.display import VirtualDisplay
# Mouse controller (decodes action dict)
from gym_csgo.glue.mouse import control_mouse, reset_mouse
# Keyboard controller (decodes action dict)
from gym_csgo.glue.keyboard import control_keyboard, reset_keyboard
# CSGO launcher
from gym_csgo.launch import launch_csgo
# Game state integration server (HTTP endpoint)
from gym_csgo.gsi import GSIServer
# Game startup arguments
from gym_csgo.specs.args import ESSENTIAL_ARGS
# Game weapon specifications
from gym_csgo.specs.weapon import NUM_WEAPON_SLOTS, observe_weapon
# Action space constructor
from gym_csgo.spaces.act import make_act_space, make_noop
# Observation space constructor
from gym_csgo.spaces.obs import make_obs_space


# Counter Strike: Global Offensive environment class
class CSGOEnv(gym.core.Env):
    # Initializes Counter-Strike environment
    def __init__(self, width=640, height=480, display_method='Xephyr',
        display=':99', gsi_path='/csgo-gsi', gsi_port=1234, args=None):
        # Immutable args parameter
        if args is None:
            args = []
        # Startup virtual display server
        self.display = VirtualDisplay(display_method, width=width,
            height=height, depth=24, display=display)
        # Setup the game state integration
        self.gsi = GSIServer(path=gsi_path, port=gsi_port)
        # Setup csgo display arguments
        display_args = [
            '-width', f'{width}', '-height', f'{height}', '-fullscreen'
        ]
        # Prepend default and append user supplied arguments
        self.csgo_args = [*ESSENTIAL_ARGS, *display_args, *args]
        # Launch csgo client session
        self.csgo_session = None
        # Collect sample screenshot
        pov = self.display.capture()
        # Setup observation space with pov shape from first real observation
        self.observation_space = make_obs_space(pov_shape=pov.shape)
        # Setup action space
        self.action_space = make_act_space()
        # Add noop action constructor
        self.action_space.noop = make_noop
        # Last observation
        self.last_obs = None
        # Current observation
        self.current_obs = None
        # Current game state
        self.current_state = None

    # Resets the environment
    def reset(self):
        # Terminate csgo client session
        if self.csgo_session:
            self.csgo_session.terminate()
        # Reset input states
        reset_keyboard(self.display.keyboard)
        reset_mouse(self.display.mouse)
        # Last observation
        self.last_obs = None
        # Current observation
        self.current_obs = None
        # Current game state
        self.current_state = None
        # Activate the virtual display
        with self.display.activate():
            # Launch new csgo client session
            self.csgo_session = launch_csgo(self.csgo_args)
        # Get first observation
        return self._get_obs()

    # Executes one action step in the environment
    def step(self, action, wait=None):
        # Send action to environment
        self._set_act(action)
        # If specified to wait for some time
        if wait is not None:
            # Sleep for requested time
            sleep(wait)
        # Collect new state observation
        obs = self._get_obs()
        # Return new (state,reward,done,info) tuple
        return obs, self._get_rew(), self._is_done(), self._get_info()

    # Closes the environment
    def close(self):
        # Terminate csgo client session
        if self.csgo_session:
            self.csgo_session.terminate()
        # Reset input states
        reset_keyboard(self.display.keyboard)
        reset_mouse(self.display.mouse)
        # Close virtual display
        self.display.close()

    # Renders a view of the environment
    def render(self, mode='human'):
        # Show image of current pov observation
        cv2.imshow(f'{self.__class__.__name__}', self.current_obs['pov'])
        # Do not block
        cv2.waitKey(1)

    # Collects new observation from the environment
    def _get_obs(self):
        # Wait for the environment to get ready
        while not self._is_ready() and not self._is_done():
            self.current_state = self.gsi.grab()
        # Start with observation dict only containing image observation
        obs = {'pov': self.display.capture()}
        # Get current game state
        state = self.gsi.grab()
        # Get player data
        player = state.player
        # Extract player state data from state if present
        if player is not None and player.state is not None:
            # Add player health
            obs['health'] = player.state.health
            # Add player armor
            obs['armor'] = player.state.armor
            # Add player having helmet
            obs['helmet'] = player.state.helmet
            # Add current grenade effects on player
            obs['flashed'] = player.state.flashed
            obs['smoked'] = player.state.smoked
            obs['burning'] = player.state.burning
            # Add player money and equipment value
            obs['money'] = player.state.money
            obs['value'] = player.state.equip_value
        # Extract player stats from state if present
        if player is not None and player.match_stats is not None:
            # Number of kills by player
            obs['kills'] = player.match_stats.kills
            # Number of assists by player
            obs['assists'] = player.match_stats.assists
            # Number of deaths of player
            obs['deaths'] = player.match_stats.deaths
            # Number of MVPs
            obs['mvps'] = player.match_stats.mvps
            # Total score of player
            obs['score'] = player.match_stats.score
        # Extract player team
        obs['team'] = player.team if player.team is not None else 'none'
        # Extract player weapons
        if player is not None and player.weapons is not None:
            # Currently equipped weapon
            if player.weapons.active is not None:
                obs['weapon_active'] = observe_weapon(player.weapons.active[1])
            # Add "None-Weapon" if none equipped
            else:
                obs['weapon_active'] = observe_weapon(None)
            # Extract weapon slots
            for index in range(NUM_WEAPON_SLOTS):
                obs[f'weapon_{index}'] = observe_weapon(
                    player.weapons.slot(index)
                )
        # Remember last observation
        self.last_obs = self.current_obs
        # Set new current observation
        self.current_obs = obs
        # Set new current game state
        self.current_state = state
        # Return collected observation
        return self.current_obs

    # Sets actions (sends to environment)
    def _set_act(self, action):
        # Send actions only if env is ready
        if self._is_ready():
            # Send actions to mouse controller
            control_mouse(self.display.mouse, action)
            # Send action to keyboard controller
            control_keyboard(self.display.keyboard, action)

    # Gets reward for last step
    def _get_rew(self):
        # Difference of scores
        #   TODO: Probably not a good reward function
        return self.current_obs['score'] - self.last_obs['score']

    # Gets info useful for debugging
    def _get_info(self):
        # Get current game state
        state = self.current_state
        # Get the id of the csgo session process group
        pgid = self.csgo_session.getpgid() if self.csgo_session else None
        # Get the display number
        display = self.display.display if self.display else None
        # Return info dictionary
        return {
            'gsi': state, 'csgo_session_pgid': pgid, 'display': display
        }

    # Tests whether the environment is ready for interactions
    def _is_ready(self):
        # Get current game state
        state = self.current_state
        # For being ready, the map needs to have a phase and players activity
        # needs to be 'playing'
        return state is not None and state.map is not None \
            and state.map.phase == 'live' and state.player.activity == 'playing'

    # Tests whether the environment is done
    def _is_done(self):
        # Get current game state
        state = self.current_state
        # Environment is done, if map phase is 'gameover'
        return state is not None and state.map is not None \
            and state.map.phase == 'gameover'


# Counter Strike: Global Offensive casual game mode environment class
class CSGOCasualEnv(CSGOEnv):
    # Constructs a casual game mode environment
    def __init__(self, mapname='de_dust2', args=None, **kwargs):
        # If no further args supplied, use empty list
        if args is None:
            args = []
        # Casual game mode config
        from gym_csgo.specs.game_modes import CASUAL
        # Construct environment using base class constructor
        super().__init__(args=['+map', mapname, *CASUAL, *args], **kwargs)


# Counter Strike: Global Offensive deathmatch game mode environment class
class CSGODeathmatchEnv(CSGOEnv):
    # Constructs a deathmatch game mode environment
    def __init__(self, mapname='de_dust2', args=None, **kwargs):
        # If no further args supplied, use empty list
        if args is None:
            args = []
        # Casual game mode config
        from gym_csgo.specs.game_modes import DEATHMATCH
        # Construct environment using base class constructor
        super().__init__(args=['+map', mapname, *DEATHMATCH, *args], **kwargs)
