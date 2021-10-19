"""
test that get_most_critical_neighbor of Agent work as intended
"""
from unittest import TestCase, main

from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment

class SimpleAgent(Agent):
    def set_criticality(self, i):
        self._Agent__criticality = i


class TestAgentGetMostCriticalNeighbor(TestCase):
    """
    Test class for Agent get_most_critical_neighbor
    """

    def test_get_most_critical_neighbor(self):
        Agent.reset_agent()
        environment = Environment()
        amas = Amas(environment)

        agent = SimpleAgent(amas)
        agent.set_criticality(30)

        n1 = SimpleAgent(amas)
        n1.set_criticality(5)
        agent.add_neighbour(n1)

        n2 = SimpleAgent(amas)
        n2.set_criticality(10)
        agent.add_neighbour(n2)

        n3 = SimpleAgent(amas)
        n3.set_criticality(15)
        agent.add_neighbour(n3)

        n4 = SimpleAgent(amas)
        n4.set_criticality(25)
        agent.add_neighbour(n4)

        self.assertEqual(agent.get_most_critical_neighbor(False), n4)

    def test_get_most_critical_neighbor_with_self(self):
        Agent.reset_agent()
        environment = Environment()
        amas = Amas(environment)

        agent = SimpleAgent(amas)
        agent.set_criticality(30)

        n1 = SimpleAgent(amas)
        n1.set_criticality(5)
        agent.add_neighbour(n1)

        n2 = SimpleAgent(amas)
        n2.set_criticality(10)
        agent.add_neighbour(n2)

        n3 = SimpleAgent(amas)
        n3.set_criticality(15)
        agent.add_neighbour(n3)

        n4 = SimpleAgent(amas)
        n4.set_criticality(25)
        agent.add_neighbour(n4)

        self.assertEqual(agent.get_most_critical_neighbor(True), agent)


if __name__ == '__main__':
    main()
