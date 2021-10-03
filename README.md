# gym-csgo
Counter-Strike: Global Offensive environment for OpenAI Gym on Linux

:bangbang: **Never use this connecting to official/online game servers! Never cheat! It _might_ get you banned.**

:bangbang: **Consider creating a separate throwaway steam account for experimenting with this environment.**

# Prerequisites
To use the gym environment, steam for Linux with Counter-Strike: Global
Offensive installed needs to be available.
            
As the native (Linux, using OpenGL) version of Counter-Strike: Global Offensive
does not get hardware acceleration in virtual X servers like `Xvfb` or `Xephyr`,
it is necessary to run the game in compatibility mode,  to get reasonable
performance (frames per second) in the gym environment: Using the steam client,
in the **Properties** of Counter-Strike: Global Offensive navigate to
**Compatibility** and check **Force the use of a specific Steam Play
compatibility tool** and select **Proton 5.13-6** (others might work but are not
tested) from the drop-down menu below.
> As of 1 October 2021 **Proton 6.3-6** is longer available in the steam
> client. Using **6.3-7** the game keeps crashing just after startup, thus
> **5.13-6** seems to be the best option for now.

It should be possible to launch Counter-Strike: Global Offensive (App ID 730)
from the terminal (this might take some time, especially the first start after
updating or setting the compatibility):
```
steam -applaunch 730 -insecure -untrusted -novid -nojoy
```

## Game State Integration
Counter-Strike: Global Offensive Game State Integration is necessary to
communicate information about the current game state to the python interface.
This needs to be set up in the game configurations: Copy the game state
integration [configuration file](cfg/gamestate_integration_gym_csgo.cfg) from
the `cfg` directory of the repository into the `cfg` directory of the
Counter-Strike: Global Offensive installation.

To find out more about the Counter-Strike: Global Offensive Game State
Integration and its configuration look at the [Valve Developer
Community](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration).

## Virtual Display
The gym environment executes the game on a virtual X server display, either
inside a window on the pre-existing X display (`Xephyr`) or invisible in the
background (`Xvfb`). To install the required packages on **Ubuntu**:
```
sudo apt install xvfb xserver-xephyr
```

# Installation
> Note: This package is still in early stages of development, installing might
> miss dependencies or does not work at all.
```
pip install --upgrade gym-csgo
```

# Basic Usage
Running a **Deathmatch** (game mode) environment with default configuration and
random actions per step until it is done (the match is done after 10 minutes):
```python
# gym_csgo registers the envs (to gym.make(...))
import gym_csgo
# Gym environments
import gym

# Open new environment context (automatically closes env at end of scope)
with gym.make('csgo_dm-v0') as env:
    # Reset the environment
    env.reset()
    # Env is not done yet
    done = False
    # Until the environment is done
    while not done:
        # Get random action from environment
        action = env.action_space.sample()
        # Execute the random action and collect observation
        obs, rew, done, info = env.step(action)
```

# Demo Actors
Programs showing demo actors in the environment are provided in the
`gym_csgo.demo` subpackage. There are `random` and `noop` actors which sample
random actions from the environment's action space or do no action at all: These
might be useful for testing the environment in general (esp. functionality,
startup, graphics, etc.) or experiment with configuration options which can
passed to the game. Start a random actor playing a deathmatch and show the
frames per second to evaluate the performance:
```
python -m gym_csgo.demo.random csgo_dm-v0 de_dust2 +cl_showfps 1
```

A special case is the `manual` actor which allows to actually play the game
through a pygame display interacting with the gym environment which itself wraps
the game on the virtual display. This is merely a technical demonstration but
might as well be suited as a starting point for collecting human demonstration
data. Play a game of casual game mode on the map train (the pygame actor will be
available once the match starts after the warmup period):
```
python -m gym_csgo.demo.manual csgo_casual-v0 de_train
```
