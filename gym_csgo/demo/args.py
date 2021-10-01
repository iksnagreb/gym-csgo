# Command line argument parser
import argparse


# Constructs argument parser parsing all arguments required for CSGOEnv
def make_argparse():
    # Setup command line argument parser
    parser = argparse.ArgumentParser()
    # Positional arguments (all but env_id are optional)
    parser.add_argument(
        'env_id', type=str, choices=('csgo_dm-v0', 'csgo_casual-v0')
    )
    parser.add_argument(
        'mapname', type=str, nargs='?', default='de_dust2'
    )
    parser.add_argument(
        'args', type=str, nargs='*'
    )
    # Display configuration (optional with defaults)
    parser.add_argument(
        '--width', type=int, default=640
    )
    parser.add_argument(
        '--height', type=int, default=480
    )
    parser.add_argument(
        '--display', type=str, default=':99'
    )
    parser.add_argument(
        '--display-method', type=str, choices=('Xvfb','Xephyr'), default='Xvfb'
    )
    # Game State Integration configuration (optional with defaults)
    parser.add_argument(
        '--gsi-path', type=str, default='/csgo-gsi'
    )
    parser.add_argument(
        '--gsi-port', type=int, default=1234
    )
    # Return constructed argument parser
    return parser
