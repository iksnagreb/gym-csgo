# r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth


# Game state integration round descriptor
class Round(dict):
    # The phase of the current round. Value is freezetime during the initial
    # freeze time as well as team timeouts, live when the round is live, and
    # over when the round is over and players are waiting for the next round to
    # begin.
    @property
    def phase(self):
        return self.get('phase')

    # The winning team of the round.
    @property
    def win_team(self):
        return self.get('win_team')

    # The current state of the bomb. This section will not appear until the bomb
    # has at least been planted.
    @property
    def bomb(self):
        return self.get('bomb')
