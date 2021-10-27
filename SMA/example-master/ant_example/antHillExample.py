"""
class antHillExample
"""
from pyAmakCore.classes.amas import Amas

from antExample import AntExampleV1
from antExample2 import AntExampleV2
from antExample3 import CommunicatingAnt
from antExample4 import TestAnt


class AntHillExample(Amas):

    def __init__(self, env, execution_policy):
        super().__init__(env, execution_policy)

    def on_initialization(self) -> None:
        # self.set_do_log(True)
        self.add_ignore_attribute("_CommunicatingAgent__mailbox")

    def on_initial_agents_creation(self) -> None:
        for i in range(50):
            self.add_agent(AntExampleV1(self, self.get_environment().xmax/2, self.get_environment().ymax/2))
            # self.add_agent(AntExampleV2(self, self.get_environment().xmax/2, self.get_environment().ymax/2))
            # self.add_agent(CommunicatingAnt(self, self.get_environment().xmax / 2, self.get_environment().ymax / 2))
            # self.add_agent(TestAnt(self, self.get_environment().xmax / 2, self.get_environment().ymax / 2))
