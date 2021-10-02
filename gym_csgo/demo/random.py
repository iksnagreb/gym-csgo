# Gym environments, csgo to register envs
import gym, gym_csgo
# Command line argument parsing
from .args import make_argparse


# Main function entry point (do not want to have stuff in global scope)
def main(env_id, mapname, **kwargs):
    # Open new environment context (automatically closes env at end of scope)
    with gym.make(env_id, mapname=mapname, **kwargs) as env:
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
            # Show current observation (image)
            env.render()


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
