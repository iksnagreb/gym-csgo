# Environment variable
from os import environ
# Caching the display properties for increased performance
from functools import cached_property
# Starting a subprocess
from subprocess import Popen
# Context (with statement)
from contextlib import contextmanager
# Numpy arrays
import numpy as np
# Import mss screen capture
import mss
# Import pynput mouse subpackage
from pynput import mouse
# Import pynput keyboard subpackage
from pynput import keyboard


# Virtual display interface
class VirtualDisplay:
    # Registry of known display methods
    _registry = {}

    # Initializes subclasses to add to registry of implemented virtual display
    # setup methods
    def __init_subclass__(cls, method, **kwargs):
        super().__init_subclass__(**kwargs)
        # Add construction method to known display methods
        cls._registry[method] = cls

    # Constructs a class of given method
    def __new__(cls, method, display, *args, **kwargs):
        # Lookup class implementing method in registry
        subclass = cls._registry[method]
        # Construct instance of selected subclass
        obj = object.__new__(subclass)
        # Set empty display number and display process
        obj.display = display
        obj.x = None
        # Return constructed object
        return obj

    # Initializes an virtual display
    def __init__(self, method, display, *args, **kwargs):
        # Store method selector
        self.method = method
        # Set empty display number and display process
        self.display = display
        self.x = None

    # Gets pynput mouse controller for controlling the virtual display
    @cached_property
    def mouse(self):
        # Remember currently active display
        DISPLAY = environ['DISPLAY']
        # Activate the virtual display
        environ['DISPLAY'] = self.display
        # Create mouse controller connected to the virtual display (this reads
        # current environ['DISPLAY']
        controller = mouse.Controller()
        # Reset active display
        environ['DISPLAY'] = DISPLAY
        # Return mouse controller object
        return controller

    # Gets pynput keyboard controller for controlling the virtual display
    @cached_property
    def keyboard(self):
        # Remember currently active display
        DISPLAY = environ['DISPLAY']
        # Activate the virtual display
        environ['DISPLAY'] = self.display
        # Create keyboard controller connected to the virtual display (this
        # reads current environ['DISPLAY']
        controller = keyboard.Controller()
        # Reset active display
        environ['DISPLAY'] = DISPLAY
        # Return keyboard controller object
        return controller

    # Gets mss screen for capturing the virtual display
    @cached_property
    def screen(self):
        # Return mss screen capture object
        return mss.mss(display=self.display)

    # Captures an image of the virtual screen
    def capture(self):
        # Grab current screen output and convert to numpy (compatible with cv2)
        return np.array(self.screen.grab(self.screen.monitors[0]))[:, :, :3]

    # Activates the display
    @contextmanager
    def activate(self):
        # Remember currently active display
        DISPLAY = environ['DISPLAY']
        # Activate the virtual display
        environ['DISPLAY'] = self.display
        # Back to call side (with statement)
        yield
        # Reset active display
        environ['DISPLAY'] = DISPLAY

    # Closes virtual display
    def close(self):
        # If there is a virtual display process
        if self.x is not None:
            # Terminate display process
            self.x.terminate()
            # Reset display process
            self.x = None


# Virtual display class using Xvfb method
class XvfbVirtualDisplay(VirtualDisplay, method='Xvfb'):
    # Initializes the virtual display
    def __init__(self, method, width=640, height=480, depth=24, display=':99'):
        super().__init__(method, display)
        # Store display number
        self.display = display
        # Start virtual display process depending on method
        self.x = Popen(['Xvfb', display, '-screen', '0',
            f'{width}x{height}x{depth}'])


# Virtual display class using Xephyr method
class XephyrVirtualDisplay(VirtualDisplay, method='Xephyr'):
    # Initializes the virtual display
    def __init__(self, method, width=640, height=480, depth=24, display=':99'):
        super().__init__(method, display)
        # Store display number
        self.display = display
        # Start virtual display process depending on method
        self.x = Popen(['Xephyr', display, '-screen',
            f'{width}x{height}x{depth}'])
