from pyAmakCore.classes.communicating_agent import CommunicatingAgent, Mail, Mailbox



class Ampoule(CommunicatingAgent) :
    _lum = None

    def __init__(self, state, x, y, env, Mailbox, zone, maxLum, minLum):
        super().__init__()
        self._state = state #luminosite (0-100)
        self._position = [x, y]
        self._salle = env
        self._zone = zone
        self._maxLum = maxLum
        self._minLum = minLum
        self._Mailbox = Mailbox


    def get_state(self):
        return self._state

    def get_position(self):
        return self._position


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

    def on_decide(self):
        if self._lum < self._minLum :
            print ("Le volet doit agir avant moi")
        elif self._lum > self._maxLum :
            print ("")


    def on_act():
        pass
    
   