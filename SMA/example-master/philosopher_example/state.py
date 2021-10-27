from enum import *
class State(Enum):
        """
        The scheduler_tool is running
        """
        THINK = auto()

        """
        The scheduler_tool is paused
        """
        HUNGRY = auto()

        """
        The scheduler_tool is expected to stop at the end at the current cycle
        """
        EATING = auto()
