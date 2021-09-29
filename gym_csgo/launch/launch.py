# Launch subprocesses
import subprocess


# Wraps csgo process group (session)
class CSGOSessionWrapper():
    # Constructs wrapper of Popen object
    def __init__(self, popen):
        self.popen = popen

    # Terminates process group
    def terminate(self):
        # Import os functions and signal number
        import os, signal
        # Kill process group of popen object with SIGTERM
        os.killpg(os.getpgid(self.popen.pid), signal.SIGTERM)

    # Kills process group
    def kill(self):
        # Import os functions and signal number
        import os, signal
        # Kill process group of popen object with SIGKILL
        os.killpg(os.getpgid(self.popen.pid), signal.SIGKILL)

    # Gets the id of the process group
    def getpgid(self):
        # Import os functions and signal number
        import os
        # Get group id of child process
        return os.getpgid(self.popen.pid)


# Launch Counter Strike: Global Offensive in subprocess
def launch_csgo(args=None):
    # Immutable argument
    if args is None:
        args = []
    # Launch Counter Strike process via steam
    p = subprocess.Popen(['steam', '-applaunch', '730', *args],
                         start_new_session=True)
    # Return subprocess (e.g. to terminate later) wrapper
    return CSGOSessionWrapper(p)
