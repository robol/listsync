class StaticSource():

    def __init__(self, emails):
        self._emails = emails

    def get_members(self, filter = None):
        return self._emails