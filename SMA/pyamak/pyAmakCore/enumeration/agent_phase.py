"""
Agent phases
"""
from enum import Enum, auto


class Phase(Enum):
    """
    Agent is perceiving
    """
    PERCEPTION = auto()

    """
    Agent is deciding and acting
    """
    DECISION_AND_ACTION = auto()

    """
    Agent haven't started to perceive, decide or act
    """
    INITIALIZING = auto()

    """
    Agent is ready to decide
    """
    PERCEPTION_DONE = auto()

    """
    Agent is ready to perceive or die
    """
    DECISION_AND_ACTION_DONE = auto()
