"""
Amas Class
"""
from typing import List

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.tools.loggable import Loggable
from pyAmakCore.classes.tools.schedulable import Schedulable
from pyAmakCore.classes.environment import Environment
from pyAmakCore.classes.agent import Agent
from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy
from pyAmakCore.exception.override import ToOverrideWarning


class Amas(Schedulable, Loggable):
    """
    Amas Class
    """

    def __init__(self,
                 environment: Environment,
                 execution_policy: ExecutionPolicy = ExecutionPolicy.ONE_PHASE
                 ) -> None:

        Schedulable.__init__(self)
        Loggable.__init__(self)
        self.__environment: Environment = environment

        self.__agents: List[Agent] = []
        self.__agent_to_add: List[Agent] = []
        self.__agent_to_remove: List[Agent] = []

        self.__execution_policy: ExecutionPolicy = execution_policy

        self.on_initialization()
        self.on_initial_agents_creation()

    def add_pending_agent(self) -> List[Agent]:
        """
        add pending agent into agent and return added agents
        """
        for agent in self.__agent_to_add:
            agent.compute_criticality()
            self.__agents.append(agent)
        tmp = self.__agent_to_add
        self.__agent_to_add = []
        return tmp

    def remove_pending_agent(self) -> List[Agent]:
        """
        add pending agent into agent and return removed agents
        """
        for agent in self.__agent_to_remove:
            self.__agents.remove(agent)
        tmp = self.__agent_to_remove
        self.__agent_to_remove = []

        return tmp

    def add_agent(self, agent: Agent) -> None:
        """
        add agent in the amas agents list without duplicate
        """
        if agent in self.__agents:
            return
        if agent in self.__agent_to_add:
            return
        self.__agent_to_add.append(agent)

    def add_agents(self, agents: List[Agent]) -> None:
        """
        add each agent from agents in the amas agents list without duplicate
        """
        for agent in agents:
            self.add_agent(agent)

    def remove_agent(self, agent: Agent) -> None:
        """
        remove agent from amas
        """
        if agent not in self.__agents:
            return
        if agent in self.__agent_to_remove:
            return
        self.__agent_to_remove.append(agent)

    def get_environment(self) -> Environment:
        """
        return environment of amas
        """
        return self.__environment

    def get_agents(self) -> List[Agent]:
        """
        return a list of all agent
        """
        return self.__agents

    def get_execution_policy(self) -> ExecutionPolicy:
        """
        return current ExecutionPolicy of the system
        """
        return self.__execution_policy

    def on_initial_agents_creation(self) -> None:
        """
        This method is called at the end of __init__()
        """
        ToOverrideWarning("on_initial_agents_creation")
