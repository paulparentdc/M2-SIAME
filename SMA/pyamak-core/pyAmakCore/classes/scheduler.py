"""
Scheduler class
"""
from typing import List

import sys
import pathlib
from threading import Thread

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.thread_tool.schedulable_thread import SchedulableThread
from pyAmakCore.classes.thread_tool.amas_thread import AmasThread
from pyAmakCore.classes.tools.schedulable import Schedulable
from pyAmakCore.classes.scheduler_tool.scheduler_core import SchedulerCore


class Scheduler(SchedulerCore):
    """
    Scheduler class, to make sure that environment and amas are always sync together
    """

    def __init__(self, amas: Amas) -> None:
        SchedulerCore.__init__(self, amas)

        self.__schedulables: List[SchedulableThread] = []
        self.__schedulables_threads: List[Thread] = []

        self.__add_schedulables(amas, AmasThread)
        self.__add_schedulables(amas.get_environment(), SchedulableThread)

    def __add_schedulables(self, schedulable: Schedulable, cls) -> None:
        """
        add a schedulable in scheduler
        """
        schedulable_thread = cls(schedulable)
        self.__schedulables.append(schedulable_thread)
        current_thread = Thread(target=schedulable_thread.run)
        self.__schedulables_threads.append(current_thread)
        current_thread.start()

    def __wait_schedulables(self) -> None:
        """
        wait for all schedulable to release a token
        """
        for schedulable in self.__schedulables:
            schedulable.action_done.acquire()

    def __start_schedulables(self) -> None:
        """
        wait for all schedulable to release a token
        """
        for schedulable in self.__schedulables:
            schedulable.is_waiting.release()

    def first_part(self) -> None:
        """
        first part of a cycle
        """
        self.__start_schedulables()
        # on cycle begin
        self.__wait_schedulables()

    def main_part(self) -> None:
        """
        main part of a cycle
        """
        self.__start_schedulables()
        # agent cycle
        self.__wait_schedulables()

    def last_part(self) -> None:
        """
        last part of a cycle
        """
        self.__start_schedulables()
        # on cycle end
        self.__wait_schedulables()

    def run(self) -> None:
        """
        override super run to close child thread before stopping
        """
        super().run()
        self.__close_child()

    def __close_child(self) -> None:
        """
        tell all child to shut down
        """
        for schedulable in self.__schedulables:
            schedulable.exit_bool = True
            schedulable.is_waiting.release()
        for thread in self.__schedulables_threads:
            thread.join(0)
