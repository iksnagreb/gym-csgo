# r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth


# Game state integration bomb descriptor
class Bomb(dict):
    # The current state of the bomb. Values are "carried", "dropped",
    # "planting", "planted", "defusing", and "defused"
    @property
    def state(self):
        return self.get('state')

    # The current position of the bomb on the map, in x, y, z coordinates.
    @property
    def position(self):
        # Query position field (holds string, might not exist)
        position = self.get('position')
        # If position field exists
        if position is not None:
            # Split coordinates and convert to float
            return list(map(float, position.split(',')))
        # No bomb position
        return None

    # The bomb's countdown timer. Used as regular bomb timer when
    # state = planted, time until bomb plant when state = planting, and time
    # until defuse when state = defusing.
    @property
    def countdown(self):
        return self.get('countdown')

    # The SteamID of the player interacting with the bomb, in SteamID64 format.
    # The interacting player can be the player carrying the bomb
    # (state = carried), planting the bomb (state = planting), or defusing the
    # bomb (state = defusing).
    @property
    def player(self):
        return self.get('player')
