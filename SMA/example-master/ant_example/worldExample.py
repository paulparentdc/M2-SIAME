"""
Class worldExample
"""
from pyAmakCore.classes.environment import Environment


class WorldExample(Environment):

    def __init__(self, xmin, xmax, ymin, ymax, field_of_view, coef_deplacement):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        self.field_of_view = field_of_view
        self.coef_deplacement = coef_deplacement
        super().__init__()
