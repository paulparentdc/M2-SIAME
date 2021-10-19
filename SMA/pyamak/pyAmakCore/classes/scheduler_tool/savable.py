"""
Savable Class
"""
import pickle

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.scheduler_tool.scheduler_state import State


class Savable:
    """
    Class that implement convenient method to save and load an amas
    """

    def __init__(self, amas: Amas) -> None:
        self.amas: Amas = amas
        self.state: State = State.RUNNING
        self.save_path = None

    def get_amas(self):
        """
        return amas
        """
        return self.amas

    def _dump(self, file):
        """
        Save the current state of the system
        """
        with open(file, 'wb') as handle:
            pickle.dump(self.amas, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def save(self, file="filename.pickle") -> None:
        """
        try to save if scheduler is not working
        """

        if self.state == State.RUNNING:
            self.save_path = file
            self.state = State.NEED_TO_SAVE
        if self.state == State.WAITING:
            self._dump(file)

    @classmethod
    def load(cls, file="filename.pickle") -> 'Savable':
        """
        Load the last save of the system
        """
        with open(file, 'rb') as handle:
            amas_object = pickle.load(handle)

        return cls(amas_object)
