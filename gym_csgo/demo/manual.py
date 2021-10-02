# Interactive game window
import pygame
# Image processing
import cv2
# Gym environments, csgo to register envs
import gym, gym_csgo
# Command line argument parsing
from .args import make_argparse


# Key binding (keyboard layout, pygame - CSGO action mapping)
def map_keys_to_action(keys, action: dict):
    # Mapping dictionary:
    #   Lookup pygame key for each available action
    mappings = {
        'forward': pygame.K_w,
        'left': pygame.K_a,
        'back': pygame.K_s,
        'right': pygame.K_d,
        'jump': pygame.K_SPACE,
        'walk': pygame.K_LSHIFT,
        'duck': pygame.K_LCTRL,
        'reload': pygame.K_r,
        'drop': pygame.K_g,
        'use': pygame.K_e,
        'switch': pygame.K_q,
        'healthshot': pygame.K_x
    }
    # Iterate all actions and test whether the mapped key is set
    for key in mappings:
        action[key] = keys[mappings[key]]
    # Equip weapon selections
    selections = [
        pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
        pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9
    ]
    # Iterate all selections and set the equip action
    for (index,key) in enumerate(selections):
        # If the key is pressed
        if keys[key]:
            # Update equipment selection with index
            action["equip"] = index
    # Return updated action
    return action


# Maps mouse state to action
def map_mouse_to_action(mouse, action, scale=50, limit=480):
    # Get mouse movement since last step
    (x, y) = mouse.get_rel()
    # Set camera actions
    action["camera"][0] = min(max(scale * x, -limit), limit)
    action["camera"][1] = min(max(scale * y, -limit), limit)
    # Attack with mouse left click
    action["fire"] = mouse.get_pressed()[0]
    # Special weapon action with mouse right click
    action["special"] = mouse.get_pressed()[2]
    # Return modified action
    return action


# Main function entry point (do not want to have stuff in global scope)
def main(env_id, mapname, **kwargs):
    # Initialize pygame environment
    pygame.init()
    # Setup pygame display for input and output of the environment
    display = pygame.display.set_mode((kwargs['width'], kwargs['height']))
    # Do not grab the input (mouse constrained to the pygame display)
    pygame.event.set_grab(False)
    # Show no mouse cursor
    pygame.mouse.set_visible(False)
    # Open new environment context (automatically closes env at end of scope)
    with gym.make(env_id, mapname=mapname, **kwargs) as env:
        # Reset the environment
        env.reset()
        # Env is not done yet
        done = False
        # Until the environment is done
        while not done:
            # Query input events
            pygame.event.pump()
            # Get keyboard key states
            keys = pygame.key.get_pressed()
            # Toggle mouse grab if ESC pressed
            if keys[pygame.K_ESCAPE]:
                pygame.event.set_grab(not pygame.event.get_grab())
            # Initialize using no-operation
            action = env.action_space.noop()
            # Use keyboard input to set/unset actions
            action = map_keys_to_action(keys, action)
            # Use mouse input to update actions
            action = map_mouse_to_action(pygame.mouse, action)
            # Execute the prepared action and collect observation
            obs, rew, done, _ = env.step(action)
            # Clear the display
            display.fill((255, 255, 255))
            # Convert pov observation to use with pygame
            pov = cv2.cvtColor(obs['pov'], cv2.COLOR_BGR2RGB).swapaxes(0, 1)
            # Display pov observation on pygame display
            display.blit(pygame.pixelcopy.make_surface(pov), (0, 0))
            # Flip the display (somehow the image is rotated/flipped...)
            pygame.display.flip()
            # Show display
            pygame.display.update()


# Script entry point
if __name__ == '__main__':
    # Construct environment argument parser
    parser = make_argparse()
    # Parse supplied arguments using the parser
    args = parser.parse_args()
    # Call main function and forward the arguments
    main(
        # Environment / Map / Game Setup
        args.env_id, args.mapname, args=args.args,
        # Display Setup
        width=args.width, height=args.height, display=args.display,
        display_method=args.display_method,
        # Game State Integration Setup
        gsi_path=args.gsi_path, gsi_port=args.gsi_port,
    )
