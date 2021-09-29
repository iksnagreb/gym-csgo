# Player game state integration
from gym_csgo.gsi.player import Player


# List of known CSGO weapon names
WEAPON_NAMES = ['weapon_' + name for name in [
    'c4', 'knife', 'knife_t', 'taser', 'shield', 'bumpmine', 'breachcharge',
    'decoy', 'flashbang', 'healthshot', 'hegrenade', 'incgrenade', 'molotov',
    'smokegrenade', 'tagrenade', 'm249', 'mag7', 'negev', 'nova', 'sawedoff',
    'xm1014', 'cz75a', 'deagle', 'elite', 'fiveseven', 'glock', 'hkp2000',
    'p250', 'revolver', 'tec9', 'usp_silencer', 'ak47', 'aug', 'awp', 'famas',
    'g3sg1', 'galilar', 'm4a1', 'm4a1_silencer', 'scar20', 'sg556', 'ssg08',
    'bizon', 'mac10', 'mp5sd', 'mp7', 'mp9', 'p90', 'ump45'
]]

# List of known CSGO weapon types
WEAPON_TYPES = [
    'Pistol', 'Knife', 'Rifle', 'SniperRifle', 'Submachine Gun', 'C4', 'Grenade'
]

# Weapon slots to consider
NUM_WEAPON_SLOTS = 10

# Observes a weapon converts from GSI object to dict weapon observation
def observe_weapon(weapon: Player.Weapons.Weapon) -> dict:
    # No weapon supplied
    if weapon is None:
        return {}

    # Extracts value or return 'none' enum
    def value_or_none(value):
        return value if value is not None else 'none'

    # Construct dictionary
    return {
        # Discrete Enum values
        'name': value_or_none(weapon.name),
        'type': value_or_none(weapon.type),
        'state': value_or_none(weapon.state),
        # Continuous Box values
        'ammo_clip': value_or_none(weapon.ammo_clip),
        'ammo_clip_max': value_or_none(weapon.ammo_clip_max),
        'ammo_reserve': value_or_none(weapon.ammo_reserve)
    }
