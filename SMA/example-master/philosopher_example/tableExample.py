from forkExample import ForkExample
from pyAmakCore.classes.environment import Environment


class TableExample(Environment):

    def __init__(self):
        self._forks = []
        super().__init__()

    def on_initialization(self):
        for i in range(10):
            self._forks.append(ForkExample())

    def get_forks(self):
        """
        Return forks
        """
        return self._forks
