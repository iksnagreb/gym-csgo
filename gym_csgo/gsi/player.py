# r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth


# Game state integration player
class Player(dict):
    # Player state
    class State(dict):
        # The HP of the currently spectated player. Value 0-100.
        @property
        def health(self):
            return self.get('health')

        # The Armor of the currently spectated player. Value 0-100.
        @property
        def armor(self):
            return self.get('armor')

        # Boolean value showing whether or not the player is wearing a helmet.
        @property
        def helmet(self):
            return self.get('helmet')

        # A value showing how flashed the player is, from 0 (not flashed),
        # to 255 (fully flashed)
        @property
        def flashed(self):
            return self.get('flashed')

        # How obscured the player's vision is from smoke. Value 0-255.
        @property
        def smoked(self):
            return self.get('smoked')

        # Same as above, but for when a player is on fire. Value 0-255, however
        # only 255 (on fire) and 254-0 (not on fire) appear to be relevant, as a
        # player does not stay on fire after leaving it. Still, this value does
        # steadily decrease back down to 0 after leaving fire, which could be
        # useful in on-screen animations, etc.
        @property
        def burning(self):
            return self.get('burning')

        # Current money of the spectated player with no comma separation.
        # Value 0-16000.
        @property
        def money(self):
            return self.get('money')

        # Amount of kills for the spectated player in the current round.
        # Value 0-5 (unsure if TKs increase this value)
        @property
        def round_kills(self):
            return self.get('round_kills')

        # Amount of kills from a head shot for the spectated player in the
        # current round. Value 0-5.
        @property
        def round_killhs(self):
            return self.get('round_killhs')

        # Total value of the currently spectated player's equipment.
        @property
        def equip_value(self):
            return self.get('equip_value')

    # Player match statistics
    class MatchStats(dict):
        # Number of kills of the currently spectated player.
        @property
        def kills(self):
            return self.get('kills')

        # Number of assists.
        @property
        def assists(self):
            return self.get('assists')

        # Number of deaths.
        @property
        def deaths(self):
            return self.get('deaths')

        # Number of MVPs.
        @property
        def mvps(self):
            return self.get('mvps')

        # Current score.
        @property
        def score(self):
            return self.get('score')

    # Player weapons list
    class Weapons(dict):
        # Single weapon descriptor
        class Weapon(dict):
            # The internal name of the weapon held in the weapon slot.
            @property
            def name(self):
                return self.get('name')

            # An internally used name for the weapon skin, or "default" if no
            # skin.
            @property
            def paintkit(self):
                return self.get('paintkit')

            # Type of weapon. Can be "Pistol", "Knife", "Rifle", "SniperRifle",
            # "Submachine Gun", "C4", possibly others.
            @property
            def type(self):
                return self.get('type')

            # Current amount of ammo in the clip.
            @property
            def ammo_clip(self):
                return self.get('ammo_clip')

            # Maximum amount of ammo the clip for the weapon can hold.
            @property
            def ammo_clip_max(self):
                return self.get('ammo_clip_max')

            # Amount of extra (reserve) ammo available for the weapon.
            @property
            def ammo_reserve(self):
                return self.get('ammo_reserve')

            # Current state of the weapon, "active" if currently being used,
            # "holstered" if not.
            @property
            def state(self):
                return self.get('state')

        # Iterates all weapons
        def __iter__(self):
            return (Player.Weapons.Weapon(x) for (_, x) in self.items())

        # Gets the weapon at specified slot
        def slot(self, index):
            # Query weapon at slot
            weapon = self.get(f'weapon_{index}')
            # If weapon at the slot exists
            if weapon is not None:
                # Wrap in Weapon object
                return Player.Weapons.Weapon(weapon)
            # No weapon at the slot
            return None

        # The players active weapon
        @property
        def active(self):
            # Iterate all players weapons
            for (key, value) in self.items():
                # Test weapon state (only one should be active)
                if value['state'] == 'active':
                    # Return the active weapon
                    return key, Player.Weapons.Weapon(value)
            # No weapon is active
            return None

        # The players grenades
        @property
        def grenades(self):
            # Filter by weapon type
            data = {k: v for (k, v) in self.items() if v['type'] == 'Grenade'}
            # Create new weapons wrapper
            return Player.Weapons(data)

    # Player name
    @property
    def name(self):
        return self.get('name')

    # Player clan name
    @property
    def clan(self):
        return self.get('clan')

    # Player steamid
    @property
    def steamid(self):
        return self.get('steamid')

    # Player observer slot when spectating player
    @property
    def observer_slot(self):
        return self.get('observer_slot')

    # Player team (either 'T' or 'CT', maybe None in menu)
    @property
    def team(self):
        return self.get('team')

    # Current player activity (playing, menu or textinput)
    @property
    def activity(self):
        return self.get('activity')

    # The SteamID of the spectated player in SteamID64 format
    @property
    def spectarget(self):
        return self.get('spectarget')

    # Player position (x,y,z)
    @property
    def position(self):
        # Query position field (holds string, might not exist)
        position = self.get('position')
        # If position field exists
        if position is not None:
            # Split coordinates and convert to float
            return list(map(float, position.split(',')))
        # No player position
        return None

    # Player forward movement/direction
    @property
    def forward(self):
        # Query forward field (holds string, might not exist)
        forward = self.get('forward')
        # If forward field exists
        if forward is not None:
            # Split coordinates and convert to float
            return list(map(float, forward.split(',')))
        # No player forward
        return None

    # Player state (health, armor, flashed, ...)
    @property
    def state(self):
        # Query player state (might not exist)
        state = self.get('state')
        # If state exists, wrap in State object
        if state is not None:
            return Player.State(state)
        # No player state fields
        return None

    # Player match statistics (kills, assists, deaths, ...)
    @property
    def match_stats(self):
        # Query player match_stats (might not exist)
        match_stats = self.get('match_stats')
        # If match_stats exists, wrap in State object
        if match_stats is not None:
            return Player.MatchStats(match_stats)
        # No player match_stats fields
        return None

    # Player weapons
    @property
    def weapons(self):
        # Query player weapons (might not exist)
        weapons = self.get('weapons')
        # If weapons exists, wrap in Weapons object
        if weapons is not None:
            return Player.Weapons(weapons)
        # No player weapons fields
        return None
