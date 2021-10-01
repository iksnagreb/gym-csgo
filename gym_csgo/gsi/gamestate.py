# Provider gamestate descriptor
from .provider import Provider
# Player game state descriptor
from .player import Player
# Bomb game state descriptor
from .bomb import Bomb
# Round game state descriptor
from .round import Round
# PhaseCountdowns game state descriptor
from .phase_countdowns import PhaseCountdowns
# Map game state descriptor
from .map import Map


# Global game state root structure
class GameState(dict):
    # Initializes game state dict from data handling None
    def __init__(self, data, **kwargs):
        # If no data given
        if data is None:
            # Use empty dict
            data = {}
        # Initialize dict
        super().__init__(data, **kwargs)

    # Gets game state provider data
    @property
    def provider(self):
        # Query provider data (might not exist)
        provider = self.get('provider')
        # If provider field exists
        if provider is not None:
            # Wrap in provider object
            return Provider(provider)
        # No provider
        return None

    # Gets game state player data if present
    @property
    def player(self):
        # Query player data (might not exist)
        player = self.get('player')
        # If player field exists
        if player is not None:
            # Wrap in player object
            return Player(player)
        # No player
        return None

    # Gets game state bomb data if present
    @property
    def bomb(self):
        # Query bomb data (might not exist)
        bomb = self.get('bomb')
        # If bomb field exists
        if bomb is not None:
            # Wrap in bomb object
            return Bomb(bomb)
        # No bomb
        return None

    # Gets game state round data if present
    @property
    def round(self):
        # Query round data (might not exist)
        _round = self.get('round')
        # If round field exists
        if _round is not None:
            # Wrap in round object
            return Round(_round)
        # No round
        return None

    # Gets game state phase_countdowns data if present
    @property
    def phase_countdowns(self):
        # Query phase_countdowns data (might not exist)
        phase_countdowns = self.get('phase_countdowns')
        # If phase_countdowns field exists
        if phase_countdowns is not None:
            # Wrap in phase_countdowns object
            return PhaseCountdowns(phase_countdowns)
        # No phase_countdowns
        return None

    # Gets game state map data if present
    @property
    def map(self):
        # Query map data (might not exist)
        _map = self.get('map')
        # If map field exists
        if _map is not None:
            # Wrap in map object
            return Map(_map)
        # No map
        return None

    # Gets new game state data added this frame
    @property
    def added(self):
        # Query added data (might not exist)
        added = self.get('added')
        # If added field exists
        if added is not None:
            # Wrap in GameState object
            return GameState(added)
        # No added data
        return None

    # Gets previous data (changed this frame)
    @property
    def previously(self):
        # Query previously data (might not exist)
        previously = self.get('previously')
        # If previously field exists
        if previously is not None:
            # Wrap in GameState object
            return GameState(previously)
        # No previously data
        return None
