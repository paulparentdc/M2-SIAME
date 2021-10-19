"""
class Callable
"""
import pathlib
import sys
from threading import Semaphore


sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.scheduler_tool.scheduler_state import State
from pyAmakCore.classes.scheduler_tool.savable import Savable


class Callable(Savable):
    """
    Class that implement useful method to interact with the program
    """

    def __init__(self, amas) -> None:
        super().__init__(amas)
        self.exit_bool: bool = False
        self.sleep_time: float = 0

        self.semaphore_start_stop: Semaphore = Semaphore(0)

    def exit_program(self) -> None:
        """
        Exit the system as soon as possible
        """
        self.exit_bool = True
        self.semaphore_start_stop.release()

    def start(self) -> None:
        """
        Unlock the scheduler
        """
        self.state = State.RUNNING
        self.semaphore_start_stop.release()

    def stop(self) -> None:
        """
        Lock the scheduler
        """
        self.state = State.WAITING
        self.semaphore_start_stop.acquire()

    def set_sleep(self, sleep_time: int) -> None:
        """
        Set sleep value between 2 cycles
        """
        self.sleep_time = sleep_time
