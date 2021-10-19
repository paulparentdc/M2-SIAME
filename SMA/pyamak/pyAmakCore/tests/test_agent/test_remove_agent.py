"""
test that compute_criticality of Agent work as intended
"""
from math import inf
from unittest import TestCase, main

from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment


class TestAgentComputeCriticality(TestCase):
    """
    Test class for Agent compute_criticality
    """

    def test_compute_criticality(self):
        Agent.reset_agent()
        environment = Environment()
        amas = Amas(environment)
        agent = Agent(amas)
        self.assertEqual(agent.compute_criticality(), -inf)


if __name__ == '__main__':
    main()
