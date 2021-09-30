# gym-csgo
Counter-Strike: Global Offensive environment for OpenAI Gym on Linux

# Prerequisites
To use the gym environment, steam for Linux with Counter-Strike: Global
Offensive installed needs to be available.
            
As the native (Linux, using OpenGL) version of Counter-Strike: Global Offensive
does not get hardware acceleration in virtual X servers like `Xvfb` or `Xephyr`,
it is necessary to run the game in compatibility mode,  to get reasonable
performance (frames per second) in the gym environment: Using the steam client,
in the **Properties** of Counter-Strike: Global Offensive navigate to
**Compatibility** and check **Force the use of a specific Steam Play
compatibility tool** and select **Proton 6.3-6** (others might work but are not
tested) from the drop-down menu below.

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
> Note: This package is still in early stages of development and there are no
> other options to install besides cloning the repository for now.

First install or upgrade python packages necessary to build and install the
library. It is recommended to install into a local python environment (`venv`):
```
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip setuptools wheel
```

Now clone the git repository into the empty directory `gym-csgo` and install the
package in editable mode via pip:

```
https://github.com/iksnagreb/gym-csgo
pip install -e gym-csgo
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
