"""
Agent execution policy
"""
from enum import Enum, auto


class ExecutionPolicy(Enum):
    """
    Every agent perceives, then every agent agent decides and acts
    """
    TWO_PHASES = auto()
    """
    Every agent perceives, decides and act. When they all have finished, they start again (or die)
    """
    ONE_PHASE = auto()
