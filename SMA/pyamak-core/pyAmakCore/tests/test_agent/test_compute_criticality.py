"""
test that remove agent of Agent work as intended
"""
from unittest import TestCase, main

from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment


class TestAgentRemoveAgent(TestCase):
    """
    Test class for Agent remove agent
    """

    def test_remove_agent(self):
        Agent.reset_agent()
        environment = Environment()
        amas = Amas(environment)
        agent = Agent(amas)

        amas.add_agent(agent)
        agent.remove_agent()
        self.assertEqual(amas.get_agents(), [])


if __name__ == '__main__':
    main()
