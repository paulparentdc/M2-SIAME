from TP.ampoule import Ampoule
from pyAmakCore.classes.environment import Environment
import numpy as np
import scipy.stats

class Salle(Environment) :

    def __init__(self,heure, listeCapteursZ1, listeCapteursZ2, volets, ampoules):
        self._lumSalle = np.zeros((10,10))
        self._listeAmpoule
        self._capteursZ1 = listeCapteursZ1
        self._capteursZ2 = listeCapteursZ2
        self._heure = heure #evolue de 0 a 24
        self._volets = volets
        self._ampoules = ampoules 

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
    
    def affiche_salle(self):
        print(self._mapSalle)

    def calcul_soleil(self):
        return self._schemaSoleil[int(self._heure * 2)]


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

    def construire_modele(x, y, lum):
        map = np.zeros((10,10))
        map[x][y] = lum
        for l in range(lum, 2):
            for i in range(0, 9):
                for j in range(0, 9):
                    if(map[i][j] == l):
                        if(i+1<=9 and map[i+1][j]==0):
                            map[i+1][j] = l-1
                        if(i-1>=0 and map[i-1][j]==0):
                            map[i-1][j] = l-1
                        if(j+1<=9 and map[i][j+1]==0):
                            map[i][j+1] = l-1
                        if(j-1>=0 and map[i][j-1]==0):
                            map[i][j-1] = l-1
        return map


    def fusionner_modeles(modeles):
        modeleFinal = np.zeros((10,10))
        for i in range(0, 9):
            for j in range(0, 9):
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


def main()
    salle(0,[[0,0]],[[9,0]],volet(),Ampoule())

if __name__ == "__main__" :
    main



 
    
    