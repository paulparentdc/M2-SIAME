"""
test that agents of Amas work as intended
"""

from unittest import TestCase, main

from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment
from pyAmakCore.classes.agent import Agent

class SimplerAmas(Amas):

    def synchronization(self):
        self._Amas__scheduler.give_amas_token()
        super().synchronization()

class TestAmasAgents(TestCase):
    """
    Test class for Amas agents
    """

    def test_init_agents(self) -> None:
        """
        test that agents is empty after init
        """

        environment = Environment()
        amas = Amas(environment)
        self.assertEqual(amas.get_agents(), [])

        # agent are not auto add to amas
        agent = Agent(amas)
        self.assertEqual(amas.get_agents(), [])

    def test_add_agent(self) -> None:
        """
        test that add agent, add agent with duplicate
        """

        environment = Environment()
        amas = SimplerAmas(environment)

        agent1 = Agent(amas)
        agent2 = Agent(amas)
        agent3 = Agent(amas)
        # add 1 agent
        amas.add_agent(agent1)
        amas.add_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1])

        # don't remove previous agent
        amas.add_agent(agent2)
        amas.add_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1, agent2])

        # add agent in good order
        amas.add_agent(agent3)
        amas.add_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1, agent2, agent3])

        # don't add duplicate
        amas.add_agent(agent1)
        amas.add_agent(agent2)
        amas.add_agent(agent3)
        amas.add_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1, agent2, agent3])

    def test_add_agents(self) -> None:
        """
        test that add_agents work as intended
        """

        environment = Environment()
        amas = SimplerAmas(environment)

        agent1 = Agent(amas)
        agent2 = Agent(amas)
        agent3 = Agent(amas)
        agent4 = Agent(amas)
        agent5 = Agent(amas)

        amas.add_agents([agent1, agent2, agent3, agent4, agent5])
        amas.add_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1, agent2, agent3, agent4, agent5])

        amas = SimplerAmas(environment)
        amas.add_agents([agent1, agent2])
        amas.add_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1, agent2])

        amas.add_agents([agent1, agent2, agent4, agent2, agent3])
        amas.add_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1, agent2, agent4, agent3])

    def test_remove_agent(self) -> None:
        environment = Environment()
        amas = SimplerAmas(environment)

        agent1 = Agent(amas)
        agent2 = Agent(amas)
        agent3 = Agent(amas)

        amas.remove_agent(agent2)
        amas.remove_pending_agent()
        self.assertEqual(amas.get_agents(), [])

        amas.add_agents([agent1, agent2, agent3])
        amas.add_pending_agent()

        amas.remove_agent(agent2)
        amas.remove_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1, agent3])

        amas.remove_agent(agent2)
        amas.remove_pending_agent()
        self.assertEqual(amas.get_agents(), [agent1, agent3])

        amas.remove_agent(agent1)
        amas.remove_agent(agent3)
        amas.remove_pending_agent()
        self.assertEqual(amas.get_agents(), [])


if __name__ == '__main__':
    main()
