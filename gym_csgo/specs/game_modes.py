# Creates game mode config based on type and mode number
def game_mode( type: int, mode: int ):
    return ['+game_type', str(type), '+game_mode', str(mode)]

# Casual game mode config (list)
CASUAL = game_mode(type=0, mode=0)

# Deathmatch game mode config (list)
DEATHMATCH = game_mode(type=1, mode=2)
