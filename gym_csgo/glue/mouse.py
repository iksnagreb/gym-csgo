# Pynput library to interact with the mouse
from pynput import mouse

# Sets mouse button state
def set_button( controller, button, state ):
    # If state is True (Pressed)
    if state:
        # Press the mouse button
        controller.press(button)
    else:
        # Otherwise release the mouse button
        controller.release(button)

# Sets Counter Strike: Global Offensive mouse state
def control_mouse( controller, state ):
    # Set special state
    set_button(controller, mouse.Button.right, state['special'])
    # Set fire state
    set_button(controller, mouse.Button.left, state['fire'])
    # Move the mouse pointer (moves the game camera)
    controller.move(*state['camera'])

# Resets Counter Strike: Global Offensive mouse state
def reset_mouse( controller ):
    # Set special state
    set_button(controller, mouse.Button.right, False)
    # Set fire state
    set_button(controller, mouse.Button.left, False)
