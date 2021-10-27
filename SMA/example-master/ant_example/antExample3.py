"""
class antExample

this one use communicating agent
"""
from math import *
from random import randint

from pyAmakCore.classes.communicating_agent import CommunicatingAgent

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from color import Color


class CommunicatingAnt(CommunicatingAgent):

    def __init__(self,
                 amas: 'antHillExample',
                 startX: float,
                 startY: float
                 ) -> None:
        super().__init__(amas)
        self._dx = startX
        self._dy = startY
        self._color = Color.BLACK

    def get_color(self):
        return self._color

    def get_dx(self):
        return self._dx

    def get_dy(self):
        return self._dy


    def read_mail(self, mail: 'Mail') -> None:
        self._color = mail.get_message()

    def on_perceive(self) -> None:
        self.reset_neighbour()
        for agent in self.get_amas().get_agents():
            length = sqrt(pow(self._dx - agent.get_dx(), 2) + pow(self._dy - agent.get_dy(), 2))
            if length < self.get_environment().field_of_view:
                self.add_neighbour(agent)

    def on_act(self) -> None:
        # couleur

        if self._color == Color.BLACK:
            color = {
                1: Color.BLUE,
                2: Color.BLACK,
                3: Color.RED,
                4: Color.YELLOW,
                5: Color.GREEN
            }
            if randint(1, 100) <= 2:
                self._color = color.get(randint(1, 5))

        # déplacement
        self._dx += (randint(-1, 1) * self.get_environment().coef_deplacement)
        self._dy += (randint(-1, 1) * self.get_environment().coef_deplacement)

        if self._dx < self.get_environment().xmin:
            self._dx = self.get_environment().xmin

        if self._dx > self.get_environment().xmax:
            self._dx = self.get_environment().xmax

        if self._dy < self.get_environment().ymin:
            self._dy = self.get_environment().ymin

        if self._dy > self.get_environment().ymax:
            self._dy = self.get_environment().ymax

        if self._color != Color.BLACK:
            for neighbor in self.get_neighbour():
                self.send_message(self._color, neighbor.get_id())

