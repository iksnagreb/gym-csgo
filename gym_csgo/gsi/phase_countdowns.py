# r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth


# Game state integration phase_countdowns descriptor
class PhaseCountdowns(dict):
    # The current phase of the round. Values are similar to the "round"
    # component (live, over, freezetime), but also includes "bomb" when the bomb
    # is planted, "defuse" when the bomb is being defused, and "warmup" during
    # the pre-game warmup time.
    @property
    def phase( self ):
        return self.get('phase')
    
    # The time in which the current phase ends. This timer changes depending on
    # the phase. For example, during "live" it will display the time left in the
    # round, but when the bomb is planted it will change to display the time
    # before the bomb explodes. When the round ends and phase goes to "over", it
    # will display the time left before the new round starts.
    @property
    def phase_ends_in( self ):
        return self.get('phase_ends_in')
