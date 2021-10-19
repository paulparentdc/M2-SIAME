"""
SchedulerMono class
"""
from random import shuffle
from typing import List

import sys
import pathlib


sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakCore.classes.scheduler_tool.scheduler_core import SchedulerCore
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.tools.schedulable import Schedulable
from pyAmakCore.classes.communicating_agent import CommunicatingAgent
from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy


class SchedulerMono(SchedulerCore):
    """
    Scheduler class, without threading
    """

    def __init__(self, amas: Amas) -> None:
        SchedulerCore.__init__(self, amas)

        self.schedulables: List[Schedulable] = []

        self.schedulables.append(self.amas)
        self.amas.add_pending_agent()
        self.schedulables.append(self.amas.get_environment())

    def first_part(self) -> None:
        """
        first part of a cycle
        """
        self.amas.add_pending_agent()

        for schedulable in self.schedulables:
            schedulable.on_cycle_begin()

    def main_part(self) -> None:
        """
        main part of a cycle
        """

        def phase1(current_agent: Agent) -> None:
            """
            this is the first phase of a cycle
            """
            current_agent.next_phase()
            current_agent.on_cycle_begin()
            if isinstance(current_agent, CommunicatingAgent):
                current_agent.read_mails()

            current_agent.on_perceive()
            current_agent.set_criticality(current_agent.compute_criticality())
            current_agent.next_phase()

        def phase2(current_agent: Agent) -> None:
            """
            this is the second phase of a cycle
            """
            current_agent.next_phase()
            current_agent.on_decide()
            current_agent.on_act()
            current_agent.set_criticality(current_agent.compute_criticality())
            current_agent.next_phase()
            current_agent.on_cycle_end()

        agents: List[Agent] = self.amas.get_agents()

        if self.amas.get_execution_policy() == ExecutionPolicy.ONE_PHASE:
            shuffle(agents)
            for agent in agents:
                phase1(agent)
                phase2(agent)
        else:
            shuffle(agents)
            for agent in agents:
                phase1(agent)
            shuffle(agents)
            for agent in agents:
                phase2(agent)

    def last_part(self) -> None:
        """
        last part of a cycle
        """
        for schedulable in self.schedulables:
            schedulable.on_cycle_end()

        self.amas.remove_pending_agent()
        self.amas.to_csv(self.amas.get_cycle(), self.amas.get_agents())

        for schedulable in self.schedulables:
            schedulable.cycle()
