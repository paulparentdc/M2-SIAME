import sys
sys.path.extend(['/nfs/home/camsi8/Documents/M2-SIAME/SMA/pyamak-core'])

from pyAmakCore.classes.environment import Environment
from pyAmakCore.classes.communicating_agent import CommunicatingAgent, Mail, Mailbox
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.scheduler import Scheduler
import numpy as np
import scipy.stats

class Salle(Environment) :

    def __init__(self,heure):
        self._lumSalle = np.zeros((10,10)).astype
        self._heure      = heure #evolue de 0 a 24
        self._capteursZ1 = []
        self._capteursZ2 = []
        self._volets     = []
        self._ampoules   = []
        
        

        #Creation du schema du soleil (Gauss)
        x_min = 0.0
        x_max = 24.0

        mean = 14.0 
        std = 3.0

        x = np.linspace(x_min, x_max,48)

        y = scipy.stats.norm.pdf(x,mean,std)
        y = y*750

        self._schemaSoleil = y.astype(int)
        super().__init__()

    def on_cycle_begin(self):
        self._heure = (self._heure + 0.5) % 24
        self.maj_lumSalle()

    def on_cycle_end(self):
        self.maj_lumSalle()
        self.affiche()
        input("Press enter to continue ...")
    

    def affiche(self):
        print(self._lumSalle)

    def calcul_soleil(self):
        return self._schemaSoleil[int(self._heure * 2)]


    def ajouterVolet(self, volet):
        self._volets.append(volet)

    def ajouterAmpoule(self, ampoule):
        self._ampoules.append(ampoule)

    def ajouterCapteur(self, zone, capteur):
        if(zone == 1):
            self._capteursZ1.append(capteur)
        else:
            self._capteursZ2.append(capteur)


    def mesure_capteurs_Z1(self):
        listeMesure = []
        for c in self._capteursZ1:
            listeMesure.append(self._lumSalle[c[0]][c[1]])
        return listeMesure
    
    def mesure_capteurs_Z2(self):
        listeMesure = []
        for c in self._capteursZ2:
            listeMesure.append(self._lumSalle[c[0]][c[1]])
        return listeMesure


    def construire_modele(self, x, y, lum):
        coefDiffusion = 5
        map = np.zeros((10,10))
        map = map.astype(int)
        lum = int(lum)
        map[x][y] = lum
        
        for l in range(lum, 2, -1*coefDiffusion):
            for i in range(0, 10):
                for j in range(0, 10):
                    if(map[i][j] == l): 
                        if(i+1<=9 and map[i+1][j]==0):
                            map[i+1][j] = l-coefDiffusion
                        if(i-1>=0 and map[i-1][j]==0):
                            map[i-1][j] = l-coefDiffusion
                        if(j+1<=9 and map[i][j+1]==0):
                            map[i][j+1] = l-coefDiffusion
                        if(j-1>=0 and map[i][j-1]==0):
                            map[i][j-1] = l-coefDiffusion
        
        return map

    def fusionner_modeles(self, modeles):
        modeleFinal = np.zeros((10,10)).astype(int)
        for i in range(0, 10):
            for j in range(0, 10):
                max = 0
                for m in modeles:
                    if(m[i][j] > max):
                        max = m[i][j]
                modeleFinal[i][j] = max
            
        return modeleFinal


    def maj_lumSalle(self):
        modeles = []
        lumSoleil = self.calcul_soleil()
        #Generation des modeles des volets

        for v in self._volets:
            lumVolet =  lumSoleil * v.get_state() / 100
            positions = v.get_positions()
            
            for p in positions:
                modeles.append(self.construire_modele(p[0], p[1], lumVolet))

        #Generation des modeles des ampoules
        for a in self._ampoules:
            lumAmpoule = a.get_state()
            p = a.get_position()
            modeles.append(self.construire_modele(p[0], p[1], lumAmpoule))

        self._lumSalle = self.fusionner_modeles(modeles)








class Ampoule(CommunicatingAgent) :
    _lum = None
    _listeMesure = None

    def __init__(self, amas, state, position, salle, zone, maxLum, minLum):
        super().__init__(amas)
        self._state = state #luminosite (0-100)
        self._position = position
        self._salle = salle
        self._zone = zone
        self._maxLum = maxLum
        self._minLum = minLum
        #self._Mailbox = Mailbox


    def get_state(self):
        return self._state        

    def get_position(self):
        return self._position

    def get_conso(self):
        return (self._state ** 1.5).astype(int)

    def on_perceive(self):
        # récupère la valeur de capteur de sa zone
        if self._zone == 1:
            listeMesure = self._salle.mesure_capteurs_Z1()
        else :
            listeMesure = self._salle.mesure_capteurs_Z2()

        lumiMin = 100
        for v in listeMesure:
            if v < lumiMin :
                lumiMin = v
                
        if listeMesure:
            self._lum = 0
        self._lum = lumiMin

 
    def on_act(self):
        if self._lum < self._minLum :
            self._state += 1
            
        elif self._lum > self._maxLum :
            self._state -= 1








class Volet(CommunicatingAgent) :
    _state = None #ouverture du volet (0-100)
    _positions = None
    _lum = None

    def __init__(self, amas, state, positions, salle, zone, maxLum, minLum):
        super().__init__(amas)
        self._state = state
        self._positions = positions
        self._salle = salle
        self._zone = zone
        self._maxLum = maxLum
        self._minLum = minLum
        

    def get_positions(self):
        return self._positions

    def get_state(self):
        return self._state


    def on_perceive(self):
        if self._zone == 1:
            listeMesure = self._salle.mesure_capteurs_Z1()
        elif self._zone == 2:
            listeMesure = self._salle.mesure_capteurs_Z2()

        lumiMin = 100
        for v in listeMesure:
            if v < lumiMin :
                lumiMin = v

        if listeMesure:
            self._lum = 0
        self._lum = lumiMin

    def on_act():
        pass

    def on_decide():
        pass







class AmaSalle(Amas) :
    def __init__(self, salle):
        super().__init__(salle)

    def on_initial_agents_creation(self):
        ampoule1 = Ampoule(self, 40, [2,2], self.get_environment(), 1, 50, 40)
        ampoule2 = Ampoule(self, 100, [9,5], self.get_environment(), 2, 50, 40)
        volet1 = Volet(self, 30, [[0,9],[1,9],[2,9],[3,9],[4,9]], self.get_environment(), 1, 50, 40)
        volet2 = Volet(self, 30, [[5,9],[6,9],[7,9],[8,9],[9,9]], self.get_environment(), 2, 50, 40)
        
        self.add_agent(ampoule1)
        self.add_agent(ampoule2)
        self.add_agent(volet1)
        self.add_agent(volet2)

        self.get_environment().ajouterAmpoule(ampoule1)
        self.get_environment().ajouterAmpoule(ampoule2)
        self.get_environment().ajouterAmpoule(volet1)
        self.get_environment().ajouterAmpoule(volet2)






def main():
    salle = Salle(12)
    amaSalle = AmaSalle(salle)
    
    salle.ajouterCapteur(1, [0,0])
    salle.ajouterCapteur(2, [9,0])

    scheduler = Scheduler(amaSalle)

    scheduler.start()
    scheduler.run()

    

if __name__ == "__main__" :
    main()



 
    
    