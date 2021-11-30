from tasks import *
from outils import *


class Scheduler:
    #_tSchedule = taille du scheduler
    # pSchdule  = plus petite periode du scheduler

    def __init__(self, tasks):

        #Construction de la liste ordonée des tasks
        self._tasks = []
        while tasks:
            min = tasks[0]
            for t in tasks:
                if t.period < min.period:
                    min = t
            self._tasks.append(min)
            tasks.remove(min)
    
    
    def creer_schedule(self):
        L = []
        for t in self._tasks:
            L.append(t.period)

        self._tSchedule = ppcm(L)
        self._pSchedule = pgcd(L)

    
    def creer_jobs(self):
        self._jobs = []
        for t in self._tasks:
            for i in range(0, self._tSchedule, t.period):
                self._jobs.append([t.name, i, t.wcet])


    def construire(self):
        print(self._jobs)
        self._schedule = [[None, 0, 0], [None, self._tSchedule, 0]]
        for j in self._jobs:
            workTime = j[2]
            i = 0
            while workTime > 0:
                #On avance jusqu'à l'heure de début de notre job
                while not j[1]>=self._schedule[i][1]:
                    i += 1

                free_time = self._schedule[i+1][1] - self._schedule[i][1] - self._schedule[i][2]
                if free_time > 0:
                    if free_time >= workTime:
                        self._schedule.insert(i+1, [j[0],  self._schedule[i][1] + self._schedule[i][2], workTime] ) 
                    else:
                        self._schedule.insert(i+1, [j[0],  self._schedule[i][1] + self._schedule[i][2], free_time] ) 
                        workTime -= free_time
                
                i += 1
        
    def affiche(self):
        print(self._schedule)


