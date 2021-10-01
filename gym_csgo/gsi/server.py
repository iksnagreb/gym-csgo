"""
Counter-Strike: Global Offensive Game State Integration Server
"""

# Run server in separate thread
import threading
# HTTP server (endpoint for game state integration POST requests)
from flask import Flask, request
# Game state integration root game state descriptor
from .gamestate import GameState


# Counter Strike: Global Offensive Game State Integration Server
#   HTTP POST endpoint
class GSIServer:
    """
    HTTP POST request endpoint server for Counter-Strike: Global Offensive Game
    State Integration requests run in a separate thread.
    """

    # Configures game state integration service
    def __init__(self, path, port):
        """
        Initializes the HTTP server, current game state and thread lock for
        accessing the game state
        """
        # Current game state
        self.state = None
        # Thread lock to synchronize access to the game state
        self.lock = threading.Lock()

        # Server thread
        def server():
            # Setup flask http service
            _server = Flask(__name__)

            # Handle HTTP POST request
            @_server.route(path, methods=['POST'])
            def post():
                # Lock access to the game state
                with self.lock:
                    # Interpret request as json and write to wrapping object
                    self.state = request.get_json()
                # Send response
                return 'OK'

            # Run the flask app
            _server.run(port=port)

        # Create and start server thread
        threading.Thread(target=server, daemon=True).start()

    # Gets next game state integration if available
    def grab(self, reset=False, block=False):
        """
        Grabs the current game state.
        :param reset: Reset the state to None after the access
        :param block: Block while there is None game state
        :return: Returns the current game state as a GameState object
        """
        # Wait for new current state
        while block and not self.state:
            pass
        # Get the current state
        state = self.state
        # Reset current state (if not already being set by server thread)
        if reset and self.lock.acquire(blocking=False):
            # Set state back to None (empty)
            self.state = None
            # Release access to the game state
            self.lock.release()
        # Return the current state
        return GameState(state)

    # Streams game state integration
    def stream(self, **kwargs):
        """
        Streams (yields) game states for ever
        :param kwargs: Keyword arguments passed to the grab method
        :return: Yields the next game state as a GameState object
        """
        # Grab game states for ever
        while True:
            # Next game state
            yield self.grab(**kwargs)
