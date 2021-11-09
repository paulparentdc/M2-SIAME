from pyAmakCore.classes.agent import Agent

class Volet(Agent) :
    _state = None #ouverture du volet (0-100)
    _positions = None

    def __init__(self, state, positions):
        super().__init__()
        self._state = state
        self._position = positions

    def get_positions(self):
        return self._positions

    def get_state(self):
        return self._state

    def on_perceive():
        pass

    def on_act():
        pass

    def on_decide():
        pass
    
