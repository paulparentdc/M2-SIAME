class ForkExample:

    def __init__(self):

        self._taken_by = None

    def try_take(self, asker):
        if self._taken_by is not None:
            return False
        self._taken_by = asker
        return True

    def release(self, asker):
        if self.owned(asker):
            self._taken_by = None

    def owned(self, asker):
        if self._taken_by is None:
            return False
        return self._taken_by == asker
