"""
Environment class
"""
from random import seed

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.tools.schedulable import Schedulable


class Environment(Schedulable):
    """
    Environment class
    """

    def __init__(self, seed_int: int = None) -> None:
        self.set_seed(seed_int)
        super().__init__()
        self.on_initialization()

    def set_seed(self, number):
        """
        This method set the seed for all random in the system, it should be override to set a custom seed
        """
        if number is None:
            seed()
            return
        seed(number)
