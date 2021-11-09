from pyAmakCore.classes.agent import Agent

class Ampoule(Agent) :

    def __init__(self, state, x, y):
        super().__init__()
        self._state = state #luminosite (0-100)
        self._position = [x, y]

    def get_state(self):
        return self._state

    def get_position(self):
        return self._position

    def on_act():
        pass
    
    def on_decide():
        pass