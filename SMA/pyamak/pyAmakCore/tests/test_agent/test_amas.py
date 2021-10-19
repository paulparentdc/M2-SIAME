"""
test that amas of Agent work as intended
"""
from unittest import TestCase, main

from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment


class TestAgentAmas(TestCase):
    """
    Test class for Agent amas
    """

    def test_amas_init(self) -> None:
        """
        Test if amas is initialized properly
        """
        Agent.reset_agent()
        environment = Environment()
        amas = Amas(environment)
        agent = Agent(amas)
        self.assertEqual(agent.get_amas(), amas)


if __name__ == '__main__':
    main()
