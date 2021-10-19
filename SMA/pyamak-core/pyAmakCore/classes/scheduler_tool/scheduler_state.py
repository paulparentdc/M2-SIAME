"""
Scheduler State
"""
from enum import Enum, auto


class State(Enum):
    """
    Scheduler State
    """

    """
    Scheduler is waiting
    """
    WAITING = auto()

    """
    Scheduler is running
    """
    RUNNING = auto()

    """
    Scheduler is running and should save as soon as possible
    """
    NEED_TO_SAVE = auto()
