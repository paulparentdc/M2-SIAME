"""
Scheduler class that need to be used for pyAmakIhm
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.scheduler import Scheduler


class SchedulerIHM(Scheduler):
    """
    Convenient class to override while using pyAmakIHM
    """

    def __init__(self, amas: Amas):
        self.__observer = None
        super().__init__(amas)

    def last_part(self) -> None:
        super().last_part()
        self.__observer.updateCycle()

    def attach(self, observer: 'Controleur') -> None:
        """
        set observer pointer to observer
        """
        self.__observer = observer
