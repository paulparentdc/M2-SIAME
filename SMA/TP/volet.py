from pyAmakCore.classes.communicating_agent import CommunicatingAgent

class Volet(CommunicatingAgent) :
    _state = None #ouverture du volet (0-100)
    _positions = None
    _lum = None

    def __init__(self, state, positions, env, zone, maxLum, minLum):
        super().__init__()
        self._state = state
        self._position = positions
        self._salle = env
        self._zone = zone
        self._maxLum = maxLum
        self._minLum = minLum
        

    def get_positions(self):
        return self._positions

    def get_state(self):
        return self._state

    def on_perceive(self):
        if self._zone == "1":
            listeMesure = self._salle.mesure_capteurs_Z1()
        elif self._zone == "2":
            listeMesure = self._salle.mesure_capteurs_Z2()

        lumiMin = 100
        for v in listeMesure:
            if v < lumiMin :
                lumiMin = v

        self.lum = lumiMin

    def on_act():
        pass

    def on_decide():
        pass
    
