"""
test that environment of Agent work as intended
"""
from unittest import TestCase, main

from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment


class TestAgentEnvironment(TestCase):
    """
    Test class for Agent environment
    """

    def test_environment_init(self) -> None:
        """
        Test if environment is initialized properly
        """
        Agent.reset_agent()
        environment = Environment()
        amas = Amas(environment)
        agent = Agent(amas)
        self.assertEqual(agent.get_environment(), environment)


if __name__ == '__main__':
    main()
