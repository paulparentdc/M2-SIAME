"""
Class Agent
"""
from random import randint
from math import inf
from typing import List
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.exception.override import ToOverrideWarning
from pyAmakCore.enumeration.agent_phase import Phase


class Agent:
    """
    Class Agent
    """
    __class_id: int = 0

    def __init__(self,
                 amas: 'Amas'
                 ) -> None:
        self.__id: int = Agent.__class_id
        Agent.__class_id += 1
        self.__neighbours: List['Agent'] = []
        self.__amas: 'Amas' = amas
        self.__environment: 'Environment' = self.__amas.get_environment()
        self.__phase: Phase = Phase.INITIALIZING
        self.__criticality: float = 0

    """
    Class getter & setter
    """

    @classmethod
    def reset_agent(cls) -> None:
        """
        when reset amas, reset all agents (only ids)
        """
        Agent.__class_id = 0

    @classmethod
    def get_next_id(cls) -> int:
        """
        return next id
        """
        return Agent.__class_id

    """
    Getter & Setter
    """

    def get_id(self) -> int:
        """
        return id of agent
        """
        return self.__id

    def get_amas(self) -> 'Amas':
        """
        return amas of agent
        """
        return self.__amas

    def get_environment(self) -> 'Environment':
        """
        return environment of agent
        """
        return self.__environment

    def get_phase(self) -> Phase:
        """
        return current phase of agent
        """
        return self.__phase

    def add_neighbour(self, agent: 'Agent') -> None:
        """
        add agent into neighbours of current agent
        """
        if agent in self.__neighbours:
            return
        self.__neighbours.append(agent)

    def get_neighbour(self) -> List['Agent']:
        """
        return neighbours of agent
        """
        return self.__neighbours

    def remove_agent(self) -> None:
        """
        destroy this agent
        """
        self.__amas.remove_agent(self)

    def reset_neighbour(self) -> None:
        """
        remove all neighbours
        """
        self.__neighbours = []

    def get_criticality(self) -> float:
        """
        return criticality
        """
        return self.__criticality

    def compute_criticality(self) -> float:
        """
        compute_criticality
        """
        return -inf

    def set_criticality(self, criticality: float) -> None:
        """
        set agent criticality to criticality
        """
        self.__criticality = criticality

    def get_most_critical_neighbor(self, including_me: bool = False) -> 'Agent':
        """
        Convenient method giving the most critical neighbor at a given moment
        """
        criticalest = []
        max_criticality = -inf
        if including_me:
            criticalest.append(self)
            max_criticality = max(self.__criticality, -inf)

        for neighbour in self.__neighbours:
            if neighbour.__criticality > max_criticality:
                criticalest = [neighbour]
                max_criticality = neighbour.__criticality
            elif neighbour.__criticality == max_criticality:
                criticalest.append(neighbour)

        return criticalest[randint(0, len(criticalest) - 1)]

    def on_cycle_begin(self) -> None:
        """
        this method is called by each agent at the start of their cycle
        """
        ToOverrideWarning("on_cycle_begin")

    def on_cycle_end(self) -> None:
        """
        this method is called by each agent at the end of their cycle
        """
        ToOverrideWarning("on_cycle_end")

    def on_perceive(self) -> None:
        """
        this method is called when agent perceive
        """
        ToOverrideWarning("on_perceive")

    def on_decide(self) -> None:
        """
        this method is called when agent decide
        """
        ToOverrideWarning("on_decide")

    def on_act(self) -> None:
        """
        this method is called when agent act
        """
        ToOverrideWarning("on_act")

    def next_phase(self) -> None:
        """
        set agent phase to the next phase
        """
        next_phase = {
            Phase.INITIALIZING: Phase.PERCEPTION,
            Phase.PERCEPTION: Phase.PERCEPTION_DONE,
            Phase.PERCEPTION_DONE: Phase.DECISION_AND_ACTION,
            Phase.DECISION_AND_ACTION: Phase.DECISION_AND_ACTION_DONE,
            Phase.DECISION_AND_ACTION_DONE: Phase.PERCEPTION
        }
        self.__phase = next_phase.get(self.__phase)

    def __eq__(self, other: 'Agent') -> bool:
        # should check class
        if other is None:
            return False
        return self.__id == other.__id

    def __repr__(self):
        return str(self.__id)
