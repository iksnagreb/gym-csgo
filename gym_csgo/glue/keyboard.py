# Pynput library to interact with the keyboard
from pynput import keyboard


# Sets keyboard key state
def set_key( controller, key, state ):
    # If state is True (Pressed)
    if state:
        # Press the key
        controller.press(key)
    else:
        # Otherwise release the key
        controller.release(key)


# Sets Counter Strike: Global Offensive keyboard key state
def control_keyboard( controller, state ):
    # Set move forward state
    set_key(controller, 'W', state['forward'])
    # Set move left state
    set_key(controller, 'A', state['left'])
    # Set move back state
    set_key(controller, 'S', state['back'])
    # Set move right state
    set_key(controller, 'D', state['right'])
    # Set walk state
    set_key(controller, keyboard.Key.shift, state['walk'])
    # Set jump state
    set_key(controller, keyboard.Key.space, state['jump'])
    # Set duck state
    set_key(controller, keyboard.Key.ctrl, state['duck'])
    # Set reload state
    set_key(controller, 'R', state['reload'])
    # Set drop state
    set_key(controller, 'G', state['drop'])
    # Set use state
    set_key(controller, 'E', state['use'])
    # Set switch state
    set_key(controller, 'Q', state['switch'])
    # Set healthshot state
    set_key(controller, 'X', state['healthshot'])
    # Set equip state
    for key in range(10):
        set_key(controller, str(key), state['equip'] == key)


# Resets Counter Strike: Global Offensive keyboard key state
def reset_keyboard( controller ):
    # Set move forward state
    set_key(controller, 'W', False)
    # Set move left state
    set_key(controller, 'A', False)
    # Set move back state
    set_key(controller, 'S', False)
    # Set move right state
    set_key(controller, 'D', False)
    # Set walk state
    set_key(controller, keyboard.Key.shift, False)
    # Set jump state
    set_key(controller, keyboard.Key.space, False)
    # Set duck state
    set_key(controller, keyboard.Key.ctrl, False)
    # Set reload state
    set_key(controller, 'R', False)
    # Set drop state
    set_key(controller, 'G', False)
    # Set use state
    set_key(controller, 'E', False)
    # Set switch state
    set_key(controller, 'Q', False)
    # Set healthshot state
    set_key(controller, 'X', False)
    # Set equip state
    for key in range(10):
        set_key(controller, str(key), False)
