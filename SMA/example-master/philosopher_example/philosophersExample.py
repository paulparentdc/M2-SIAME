

from state import State
from random import randint
from pyAmakCore.classes.agent import Agent


class PhilosophersExample(Agent):
    def __init__(self, id2, amas, left, right):
        super().__init__(amas)
        self.__state = State.THINK
        self.__hungerDuration = 0
        self.__eatenPastas = 0
        self.__id2 = id2
        self.__left = left
        self.__right = right

    def on_act(self):
        next_state = self.__state
        if self.__state == State.EATING:
            self.__eatenPastas += 1
            if randint(0, 101) > 50:
                self.__left.release
                self.__right.release
                next_state = State.THINK
        else:
            if self.__state == State.HUNGRY:
                self.__hungerDuration += 1
                if self.get_most_critical_neighbor(True) == self:
                    self.__left.try_take(self)
                    self.__right.try_take(self)
                    if self.__left.owned(self) and self.__right.owned(self):
                        next_state = State.EATING
                else:
                    self.__left.release(self)
                    self.__right.release(self)
            else:
                if self.__state == State.THINK:
                    if randint(0, 101) > 50:
                        self.__hungerDuration = 0
                        next_state = State.HUNGRY
        self.__state = next_state

    def compute_criticality(self):
        if self.__state == State.HUNGRY:
            return self.__hungerDuration
        return -1

    def get_state(self):
        return self.__state

    def get_Left_Fork(self):
        if self.__left is not None:
            return self.__left

    def get_Right_Fork(self):
        if self.__right is not None:
            return self.__right
