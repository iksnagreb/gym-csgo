# Game state integration provider
class Provider(dict):
    # Provider name
    @property
    def name(self):
        return self.get('name')

    # Provider appid
    @property
    def appid(self):
        return self.get('appid')

    # Provider version
    @property
    def version(self):
        return self.get('version')

    # Provider steamid
    @property
    def steamid(self):
        return self.get('steamid')

    # Provider timestamp (unix time)
    @property
    def timestamp(self):
        return self.get('timestamp')
