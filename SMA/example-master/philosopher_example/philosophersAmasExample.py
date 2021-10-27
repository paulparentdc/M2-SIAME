from philosophersExample import PhilosophersExample
from pyAmakCore.classes.amas import Amas
from tableExample import TableExample


class PhilosophersAmasExamples(Amas):

    def __init__(self, execution_policy):
        super().__init__(TableExample(), execution_policy)

    def on_initial_agents_creation(self):
        ps = []
        for i in range(9):
            ps.append(PhilosophersExample(i, self, self.get_environment().get_forks()[i],
                                          self.get_environment().get_forks()[i + 1]))

        ps.append(
            PhilosophersExample(9, self, self.get_environment().get_forks()[9], self.get_environment().get_forks()[0]))

        for j in range(len(ps) - 1):
            ps[j + 1].add_neighbour(ps[j])
            ps[j].add_neighbour(ps[j + 1])

        ps[0].add_neighbour(ps[len(ps) - 1])
        ps[len(ps) - 1].add_neighbour(ps[0])
        self.add_agents(ps)
