from color import Color
from pyAmakIHM.classes.controleur import Controleur


class AntIHM:
    def __init__(self, agent_id, color):
        self.agent_id = agent_id
        self.color = color
        self.id_image = None


class ControleurAntsExample(Controleur):
    color_to_file = {
        Color.BLACK: 'images/blackAnt.png',
        Color.RED: 'images/redAnt.png',
        Color.GREEN: 'images/greenAnt.png',
        Color.YELLOW: 'images/yellowAnt.png',
        Color.BLUE: 'images/blueAnt.png'
    }

    def __init__(self, fenetre, amas):
        super().__init__(fenetre, amas)
        self.__ants = []
        self.__chart = []
        self.__chart.append(self.addPlotChart('Ants Position'))


    def add_ant(self, ant):
        ant_ihm = AntIHM(ant.get_id(), ant.get_color())
        ant_ihm.id_image = self.draw_image(ant.get_dx(), ant.get_dy(), ControleurAntsExample.color_to_file.get(ant_ihm.color))
        self.__ants.append(ant_ihm)

    def initialisation(self):
        self.setTitle(self.__chart[0], 'Ants Position')
        self.setXLabel(self.__chart[0], 'x')
        self.setYLabel(self.__chart[0], 'y')
        self.setPolicy(self.__chart[0], 0, 'go')

        for ant in self.get_amas().get_agents():
            self.add_ant(ant)

    def updateWindow(self):
        # TODO : remove ant in self.__ants if don't exist anymore

        # update ant
        for ant in self.get_amas().get_agents():
            seen = False
            self.addPoint(self.__chart[0], 0, ant.get_dx(), ant.get_dy())
            for ant_ihm in self.__ants:
                if ant.get_id() == ant_ihm.agent_id:
                    seen = True
                    self.move_image(ant_ihm.id_image, ant.get_dx(), ant.get_dy())
                    if ant.get_color() != ant_ihm.color:
                        self.remove_element(ant_ihm.id_image)

                        ant_ihm.color = ant.get_color()
                        ant_ihm.id_image = self.draw_image(
                            ant.get_dx(),
                            ant.get_dy(),
                            ControleurAntsExample.color_to_file.get(ant_ihm.color))
            if not seen:
                self.add_ant(ant)
