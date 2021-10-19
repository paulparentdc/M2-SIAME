"""
Schedulable interface
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from pyAmakCore.exception.override import ToOverrideWarning


class Schedulable:
    """
    Class Schedulable
    """

    def __init__(self):

        self.__nbr_cycle: int = 0

    def get_cycle(self) -> int:
        """
        return nbr_cycle
        """
        return self.__nbr_cycle

    def cycle(self) -> None:
        """
        add 1 to nbr_cycle
        """
        self.__nbr_cycle += 1

    def on_initialization(self) -> None:
        """
        This method will be executed at the end of __init__()
        """
        ToOverrideWarning("on_initialization")

    def on_cycle_begin(self) -> None:
        """
        This method will be executed at the start of each cycle
        """
        ToOverrideWarning("on_cycle_begin")

    def on_cycle_end(self) -> None:
        """
        This method will be executed at the end of each cycle
        """
        ToOverrideWarning("on_cycle_end")
