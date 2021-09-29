# HTTP server (endpoint for game state integration POST requests)
from flask import Flask, request
# Multithreading (run server in separate thread)
import threading
# Game state integration root gmae state descriptor
from .gamestate import GameState

# Counter Strike: Global Offensive Game State Integration Server
#   HTTP POST endpoint
class GSIServer( object ):
    # Configures game state integration service
    def __init__( self, path, port ):
        # Current game state
        self.state = None
        # Thread lock to synchronize access to the gamestate
        self.lock = threading.Lock()
        # Server thread
        def server(  ):
            # Setup flask http service
            server = Flask(__name__)
            # Handle HTTP POST request
            @server.route(path, methods=['POST'])
            def post(  ):
                # Lock access to the gamestate
                self.lock.acquire()
                # Interpret request as json and write to wrapping object
                self.state = request.get_json()
                # Release access to the gamestate
                self.lock.release()
                # Send response
                return 'OK'
            # Run the flask app
            server.run(port=port)
        # Create and start server thread
        threading.Thread(target=server, daemon=True).start()

    # Gets next game state integration if available
    def grab( self, reset=False, block=False ):
        # Wait for new current state
        while block and not self.state:
            pass
        # Get the current state
        state = self.state
        # Reset current state (if not already being set by server thread)
        if reset and self.lock.acquire(blocking=False):
            # Set state back to None (empty)
            self.state = None
            # Release access to the gamestate
            self.lock.release()
        # Return the current state
        return GameState(state)

    # Streams game state integration
    def stream( self, **kwargs ):
        # Grab gamestates for ever
        while True:
            # Next gamestate
            yield self.grab(**kwargs)
