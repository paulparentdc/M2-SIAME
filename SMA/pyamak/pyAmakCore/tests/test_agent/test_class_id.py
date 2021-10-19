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

    def test_id_simple(self) -> None:
        """
        Test if id is initialized properly, expected 0 the first agent, then 1 for the 2nd agents
        """
        self.assertEqual(Agent.get_next_id(), 0)

        agent1 = Agent(self.amas)
        self.assertEqual(agent1.get_id(), 0)
        self.assertEqual(Agent.get_next_id(), 1)

        agent1 = Agent(self.amas)
        self.assertEqual(agent1.get_id(), 1)
        self.assertEqual(Agent.get_next_id(), 2)

    def test_id_advanced(self) -> None:
        """
        Test if id is initialized properly, for the 10 first agents
        """
        for i in range(0, 10):
            agent1 = Agent(self.amas)
            with self.subTest(i=i):
                self.assertEqual(agent1.get_id(), i)
                self.assertEqual(Agent.get_next_id(), i + 1)


if __name__ == '__main__':
    main()
