"""
thread class for Schedulable
"""
from threading import Semaphore

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from pyAmakCore.classes.tools.schedulable import Schedulable


class SchedulableThread:
    """
    thread class used to thread schedulable
    """

    def __init__(self, schedulable: Schedulable) -> None:

        self.schedulable: Schedulable = schedulable
        self.is_waiting: Semaphore = Semaphore(0)
        self.exit_bool: bool = False
        self.action_done: Semaphore = Semaphore(0)

    def on_cycle_begin(self) -> None:
        """
        first part of the cycle
        """
        self.schedulable.on_cycle_begin()

    def main_cycle_part(self) -> None:
        """
        main part of the cycle
        """

    def on_cycle_end(self) -> None:
        """
        last part of the cycle
        """
        self.schedulable.on_cycle_end()
        self.schedulable.cycle()

    def run(self) -> None:
        """
        main part of a schedulable thread
        """
        while not self.exit_bool:
            self.is_waiting.acquire()
            if self.exit_bool:
                break
            self.on_cycle_begin()
            self.action_done.release()

            self.is_waiting.acquire()
            self.main_cycle_part()
            self.action_done.release()

            self.is_waiting.acquire()
            self.on_cycle_end()
            self.action_done.release()
