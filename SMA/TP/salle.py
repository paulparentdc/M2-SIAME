from pyAmakCore.classes.environment import Environment

class Salle(Environment) :


    def __init__(self,heure,lumi_Exter,lumi_Inter):
        self._mapSalle[[]] = None
        self._heure = heure
        self._lumi_Exter = lumi_Exter
        self._lumi_Inter = lumi_Inter
        super().__init__()

