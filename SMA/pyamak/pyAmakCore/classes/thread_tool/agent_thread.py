"""
Class Agent thread
"""
from threading import Semaphore
import sys
import pathlib


sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from pyAmakCore.classes.communicating_agent import CommunicatingAgent
from pyAmakCore.classes.agent import Agent
from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy


class AgentThread:
    """
    thread class used to thread agent
    """
    action_done = Semaphore(0)
    execution_policy = ExecutionPolicy.ONE_PHASE

    def __init__(self, agent: Agent) -> None:

        self.agent: Agent = agent
        self.is_waiting: Semaphore = Semaphore(0)
        self.exit_bool: bool = False

    def phase1(self) -> None:
        """
        this is the first phase of a cycle
        """
        if isinstance(self.agent, CommunicatingAgent):
            self.agent.read_mails()

        self.agent.on_perceive()
        self.agent.set_criticality(self.agent.compute_criticality())
        self.agent.next_phase()

    def phase2(self) -> None:
        """
        this is the second phase of a cycle
        """
        self.agent.on_decide()
        self.agent.on_act()
        self.agent.set_criticality(self.agent.compute_criticality())
        self.agent.next_phase()

    def run(self) -> None:
        """
        main part of an agent thread
        """
        while not self.exit_bool:

            self.is_waiting.acquire()
            if self.exit_bool:
                return

            self.agent.next_phase()
            self.agent.on_cycle_begin()

            self.phase1()

            if AgentThread.execution_policy == ExecutionPolicy.TWO_PHASES:
                AgentThread.action_done.release()
                self.is_waiting.acquire()

            self.agent.next_phase()

            self.phase2()

            self.agent.on_cycle_end()

            AgentThread.action_done.release()
