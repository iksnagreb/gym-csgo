# r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth


# Game state integration map descriptor
class Map(dict):
    # Map team descriptor
    class Team(dict):
        # The team's current score.
        @property
        def score(self):
            return self.get('score')

        # How many rounds the team has lost in a row.
        @property
        def consecutive_round_losses(self):
            return self.get('consecutive_round_losses')

        # The number of remaining timeouts available for the team.
        @property
        def timeouts_remaining(self):
            return self.get('timeouts_remaining')

        # How many games a team has won in a Best of X series. Only used for
        # tournaments.
        @property
        def matches_won_this_series(self):
            return self.get('matches_won_this_series')

    # Map round_wins descriptor
    class RoundWins(dict):
        # Iterates all rounds
        def __iter__(self):
            return ((_round, win) for (_round, win) in self.items())

        # Get round winning condition for round
        def round(self, index):
            return self.get(f'{index}')

    # The current game mode being played. Values can be casual, competitive,
    # deathmatch, gungameprogressive, scrimcomp2v2, possibly others.
    @property
    def mode(self):
        return self.get('mode')

    # The name of the current map.
    @property
    def name(self):
        return self.get('name')

    # The current phase of the map. Values can be warmup during the initial
    # warmup phase, live during a live game, intermission during halftime, and
    # gameover at the end of the game.
    @property
    def phase(self):
        return self.get('phase')

    # The current round number.
    @property
    def round(self):
        return self.get('round')

    # Team data
    def team(self, key):
        # Query team data (might not exist)
        team = self.get(f'team_{key.lower()}')
        # If team exists, wrap in State object
        if team is not None:
            return Map.Team(team)
        # No team fields
        return None

    # Terrorist team data
    @property
    def team_t(self):
        # Query team data (might not exist)
        team_t = self.get('team_t')
        # If team exists, wrap in State object
        if team_t is not None:
            return Map.Team(team_t)
        # No team fields
        return None

    # Counter Terrorist team data
    @property
    def team_ct(self):
        # Query team data (might not exist)
        team_t = self.get('team_ct')
        # If team exists, wrap in State object
        if team_t is not None:
            return Map.Team(team_t)
        # No team fields
        return None

    # How many matches a team has to win before winning the series.
    @property
    def num_matches_to_win_series(self):
        return self.get('num_matches_to_win_series')

    # Current number of people spectating the game.
    @property
    def current_spectators(self):
        return self.get('current_spectators')

    # How many souvenir cases were dropped this game (Probable, unconfirmed).
    @property
    def souvenirs_total(self):
        return self.get('souvenirs_total')

    # Round wins on this map
    @property
    def round_wins(self):
        # Query round_wins data (might not exist)
        round_wins = self.get('round_wins')
        # If round_wins exists, wrap in State object
        if round_wins is not None:
            return Map.RoundWins(round_wins)
        # No round_wins fields
        return None
