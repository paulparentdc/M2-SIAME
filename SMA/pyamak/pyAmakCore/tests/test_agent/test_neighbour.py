"""
test that id of Agent work as intended
"""
from unittest import TestCase, main

from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment


class TestAgentId(TestCase):
    """
    Test class for Agent id
    """
    environment = Environment()
    amas = Amas(environment)

    def setUp(self) -> None:
        Agent.reset_agent()
        self.environment = Environment()
        self.amas = Amas(self.environment)

    def test_init_neighbour(self) -> None:
        """
        Test if id is initialized properly, expected 0 the first agent, then 1 for the 2nd agents
        """
        agent = Agent(self.amas)
        self.assertEqual(agent.get_neighbour(), [])

        # don't auto add neighbour
        agent2 = Agent(self.amas)
        self.assertEqual(agent.get_neighbour(), [])
        self.assertEqual(agent2.get_neighbour(), [])

    def test_add_neighbour(self) -> None:
        """
        Test if add_neighbours work when adding agents
        """

        agent = Agent(self.amas)

        # in only 1 way
        agent2 = Agent(self.amas)
        agent.add_neighbour(agent2)
        self.assertEqual(agent.get_neighbour(), [agent2])
        self.assertEqual(agent2.get_neighbour(), [])

        # don't remove previous agent
        agent3 = Agent(self.amas)
        agent.add_neighbour(agent3)
        self.assertEqual(agent.get_neighbour(), [agent2, agent3])

        # good order
        agent4 = Agent(self.amas)
        agent.add_neighbour(agent4)
        self.assertEqual(agent.get_neighbour(), [agent2, agent3, agent4])

        # no duplicate
        agent.add_neighbour(agent2)
        agent.add_neighbour(agent3)
        agent.add_neighbour(agent4)
        self.assertEqual(agent.get_neighbour(), [agent2, agent3, agent4])

    def test_reset_neighbour(self) -> None:
        """
        Test if reset_neighbours work
        """

        # work without neighbour
        agent = Agent(self.amas)
        agent.reset_neighbour()
        self.assertEqual(agent.get_neighbour(), [])

        # work with 1 neighbour
        agent = Agent(self.amas)
        agent2 = Agent(self.amas)
        agent.add_neighbour(agent2)
        agent.reset_neighbour()
        self.assertEqual(agent.get_neighbour(), [])

        agent3 = Agent(self.amas)
        agent.add_neighbour(agent2)
        agent.add_neighbour(agent3)
        agent.reset_neighbour()
        self.assertEqual(agent.get_neighbour(), [])

        # no duplicate
        agent4 = Agent(self.amas)
        agent.add_neighbour(agent2)
        agent.add_neighbour(agent3)
        agent.add_neighbour(agent2)
        agent.add_neighbour(agent3)
        agent.add_neighbour(agent4)
        agent.reset_neighbour()
        self.assertEqual(agent.get_neighbour(), [])


if __name__ == '__main__':
    main()
