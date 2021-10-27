from pyAmakIHM.classes.controleur import Controleur
from state import State
from math import cos, sin, pi
from random import randint

class ControleurPhilosophersExample(Controleur):

    def __init__(self, fenetre, scheduler):
        super().__init__(fenetre, scheduler)
        self.__philosophers = []
        self.__left = []
        self.__right = []
        self.__numberPhilosopher = 10
        self.__chart = []
        self.__chart.append(self.addBarChart('Eaten Pastas'))
        self.__chart.append(self.addPlotChart('Hours of tkinking'))
        self.__chart.append(self.addLimitedPlotChart('Hours of tkinking (limited)',5))

        self.__hoursThinkingMr5 = 0

    def initialisation(self):

        widthCanvas = self.get_fenetre().get_canvas_width()
        heightCanvas = self.get_fenetre().get_canvas_height()


        # Init
        self.setTitle(self.__chart[0],'Eaten Pastas')
        self.setXLabel(self.__chart[0],'Philosophers')
        self.setYLabel(self.__chart[0],'Number of eaten pastas')

        self.setTitle(self.__chart[1],'Hours of thinking for Mr 4')
        self.setXLabel(self.__chart[1],'Cycle')
        self.setYLabel(self.__chart[1],'Hours')

        self.setTitle(self.__chart[2],'Hours of thinking for Mr 4 (limited)')
        self.setXLabel(self.__chart[2],'Cycle')
        self.setYLabel(self.__chart[2],'Hours')

        self.draw_text(40,15, "EATING")
        self.draw_text(40,45, "THINKING")
        self.draw_text(40,75, "HUNGRY")

        self.draw_rectangle(10, 10, 20, 20, 'green')
        self.draw_rectangle(10, 40, 20, 20, 'blue')
        self.draw_rectangle(10, 70, 20, 20, 'red')

        for i in range(self.__numberPhilosopher):
            x = 100 * cos(2 * pi * i / self.__numberPhilosopher) + (widthCanvas / 2)
            y = 100 * sin(2 * pi * i / self.__numberPhilosopher) + (heightCanvas / 2)

            carre = self.draw_rectangle(x, y, 20, 20, 'green')
            left = self.draw_rectangle(x - 15, y, 20, 7, 'black')
            right = self.draw_rectangle(x + 15, y, 20, 7, 'white')

            self.__philosophers.append(carre)
            self.__left.append(left)
            self.__right.append(right)

            nom = 'Mr ' + str(i)

            self.addColumn(self.__chart[0],nom)

    def updateWindow(self):
        agents = self.get_amas().get_agents()
        self.addPoint(self.__chart[1],0,self.get_amas().get_cycle(),self.__hoursThinkingMr5)
        self.addPoint(self.__chart[2],0,self.get_amas().get_cycle(),self.__hoursThinkingMr5)

        for i in range(10):
            state = agents[i].get_state()
            if state == State.EATING:
                self.change_color(self.__philosophers[i], 'green')
                self.increaseValue(self.__chart[0],i, 1)
                self.logsDisplay('Mr '+str(i)+' : Je mange')

            elif state == State.HUNGRY:
                self.change_color(self.__philosophers[i], 'red')

            else:
                self.change_color(self.__philosophers[i], 'blue')
                if(i == 5):
                    self.__hoursThinkingMr5 += 1

            coords = self.get_coords_element(self.__philosophers[i])
            if agents[i].get_Left_Fork().owned(agents[i]):
                self.change_color(self.__left[i],'black')
            else:
                self.change_color(self.__left[i],'white')

            if agents[i].get_Right_Fork().owned(agents[i]):
                self.change_color(self.__right[i],'black')
            else:
                self.change_color(self.__right[i],'white')

        self.errorDisplay('Controleur','Non en fait tout va bien')
