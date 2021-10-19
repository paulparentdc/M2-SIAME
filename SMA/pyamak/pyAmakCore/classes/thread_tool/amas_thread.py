"""
thread class for amas
"""
from threading import Thread
from typing import List

import sys
import pathlib


sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy
from pyAmakCore.classes.thread_tool.agent_thread import AgentThread
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.thread_tool.schedulable_thread import SchedulableThread


class AmasThread(SchedulableThread):
    """
    thread class used to thread amas
    """

    def __init__(self, amas: Amas) -> None:
        super().__init__(amas)

        self.agents: List[AgentThread] = []
        self.agents_thread: List[Thread] = []

        AgentThread.execution_policy = self.schedulable.get_execution_policy()

        self.schedulable.add_pending_agent()
        for agent in self.schedulable.get_agents():
            self.add_agent(agent)

    def add_agent(self, agent: Agent) -> None:
        """
        make agent a thread and start the thread
        """
        agent_thread = AgentThread(agent)
        self.agents.append(agent_thread)
        current_thread = Thread(target=agent_thread.run)
        self.agents_thread.append(current_thread)
        current_thread.start()

    def add_agents(self) -> None:
        """
        if there are new agents, add them
        """
        added_agent = self.schedulable.add_pending_agent()
        for agent in added_agent:
            self.add_agent(agent)

    def remove_agents(self) -> None:
        """
        if some agents are removed, close their thread
        """
        removed_agent = self.schedulable.remove_pending_agent()
        for agent in removed_agent:
            for i in range(len(self.agents)):
                if agent == self.agents[i].agent:
                    self.agents[i].exit_bool = True
                    self.agents[i].is_waiting.release()
                    self.agents_thread[i].join()

                    self.agents.remove(self.agents[i])
                    self.agents_thread.remove(self.agents_thread[i])

    def on_cycle_begin(self) -> None:
        """
        start of cycle
        """
        self.add_agents()
        self.schedulable.on_cycle_begin()

    def main_cycle_part(self) -> None:
        """
        main part of the cycle
        """
        for agent in self.agents:
            agent.is_waiting.release()
        # agent cycle

        if self.schedulable.get_execution_policy() == ExecutionPolicy.TWO_PHASES:
            # wait agents
            for i in range(len(self.agents)):
                AgentThread.action_done.acquire()
            # start phase 2 for all agents
            for agent in self.agents:
                agent.is_waiting.release()

        for i in range(len(self.agents)):
            AgentThread.action_done.acquire()

    def on_cycle_end(self) -> None:
        """
        end of cycle
        """
        self.schedulable.on_cycle_end()

        self.remove_agents()
        self.schedulable.to_csv(self.schedulable.get_cycle(), self.schedulable.get_agents())

        self.schedulable.cycle()

    def run(self) -> None:
        """
        override run so when amas_thread try to stop, he closes all agents threads
        """
        super().run()
        self.close_child()

    def close_child(self) -> None:
        """
        tell all child threads to close
        """
        for agent in self.agents:
            agent.exit_bool = True
            agent.is_waiting.release()

        for thread in self.agents_thread:
            thread.join(0)


