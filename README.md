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

        steam -applaunch 730 -insecure -untrusted -novid -nojoy

The gym environment executes the game on a virtual X server display, either
inside a window on the pre-existing X display (`Xephyr`) or invisible in the
background (`Xvfb`). To install the required packages on **Ubuntu**:

        sudo apt install xvfb xserver-xephyr
