# Launch a subprocess
import subprocess
# Import os functions
import os
# Signal number (SIGTERM)
import signal

# Wraps csgo process group (session)
class CSGOSessionWrapper():
    # Constructs wrapper of Popen object
    def __init__(self, popen):
        self.popen = popen

    # Terminates process group
    def terminate(self):
        # Kill process group of popen object with SIGTERM
        os.killpg(os.getpgid(self.popen.pid), signal.SIGTERM)

    # Kills process group
    def kill(self):
        # Kill process group of Popen object with SIGKILL
        os.killpg(os.getpgid(self.popen.pid), signal.SIGKILL)

    # Gets the id of the process group
    def getpgid(self):
        # Get group id of child process
        return os.getpgid(self.popen.pid)


# Launch Counter Strike: Global Offensive in subprocess
def launch_csgo(args=None):
    # Immutable argument
    if args is None:
        args = []
    # Launch Counter Strike process via steam
    process = subprocess.Popen(['steam', '-applaunch', '730', *args],
        start_new_session=True)
    # Return subprocess (e.g. to terminate later) wrapper
    return CSGOSessionWrapper(process)
