"""
Scheduler class
"""
from time import sleep

import sys
import pathlib

from pyAmakCore.classes.scheduler_tool.scheduler_state import State

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.scheduler_tool.callable import Callable
from pyAmakCore.classes.scheduler_tool.savable import Savable
from pyAmakCore.classes.amas import Amas


class SchedulerCore(Callable, Savable):
    """
    Core part of Scheduler
    """

    def __init__(self, amas: Amas) -> None:
        Callable.__init__(self, amas)

    def first_part(self) -> None:
        """
        first part of a cycle
        """

    def main_part(self) -> None:
        """
        main part of a cycle
        """

    def last_part(self) -> None:
        """
        last part of a cycle
        """

    def try_to_save(self):
        """
        try to save scheduler if need to
        """
        if self.state == State.NEED_TO_SAVE:
            self._dump(self.save_path)

    def run(self) -> None:
        """
        main part of amak core
        """
        while not self.exit_bool:
            print("Cycle : ", self.amas.get_cycle())

            self.try_to_save()
            self.semaphore_start_stop.acquire()
            if self.exit_bool:
                break
            self.semaphore_start_stop.release()

            self.first_part()
            self.main_part()
            self.last_part()

            self.try_to_save()
            sleep(self.sleep_time)
