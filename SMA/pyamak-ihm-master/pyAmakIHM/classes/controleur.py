"""
Class Controleur
"""

import os, sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakIHM.classes.fenetre import Fenetre
from threading import Thread

class Controleur:
    """
    Class Controleur
    """

    def __init__(
        self,
        fenetre : 'Fenetre',
        scheduler : 'SchedulerIHM'
    ) -> None :
        self.__th = None
        self.__fenetre = fenetre
        self.__fenetre.attach(self)

        self.__scheduler = scheduler
        self.__scheduler.attach(self)
        self.__amas = scheduler.get_amas()

        self.__is_run = False

    def get_fenetre(self) -> 'Fenetre':
        return self.__fenetre

    def get_amas(self) -> 'Amas':
        return self.__amas

    def get_scheduler(self) -> 'SchedulerIHM':
        return self.__scheduler

    """
    Draw a rectangle with x,y coords, height, width and color
    """
    def draw_rectangle(self, x : float, y : float, height : float, width : float, color : str) -> int:
        return self.__fenetre.draw_rectangle(x, y, height, width, color)

    """
    Draw a circle with x,y coords, radian and color
    """
    def draw_circle(self, x : float, y : float, radian : float, color : str):
        return self.__fenetre.draw_circle(x, y, radian, color)

    """
    Draw a line between x0,y0 and x1,y1 point with color
    """
    def draw_line(self, x0 : float, y0 : float, x1 : float, y1 : float, color : str) -> int:
        return self.__fenetre.draw_line(x0,y0,x1,y1,color)

    """
    Draw an image with x,y coords and its name
    """
    def draw_image(self, x : float, y : float, fileName : str) -> int:
        return self.__fenetre.draw_image(x, y, fileName)

    """
    Draw a text with x,y coords
    """
    def draw_text(self, x : float, y : float, text : str) -> int:
        return self.__fenetre.draw_text(x,y,text)

    """
    Move an image to x,y coords
    """
    def move_image(self, image : int, x : float, y : float) -> None:
        self.__fenetre.move_image(image, x, y)

    """
    Move an element to x,y coords
    """
    def move_element(self, element : int, x : float, y : float) -> None:
        self.__fenetre.move_element(element,x,y)

    """
    Remove an element
    """
    def remove_element(self, element : int) -> None:
        self.__fenetre.remove_element(element)

    """
    Remove all element
    """
    def remove_all(self) -> None:
        self.__fenetre.remove_all()


    """
    Give the element's coords
    """
    def get_coords_element(self, element : int) -> (float,float):
        return self.__fenetre.get_coords_element(element)

    """
    Give the image's coords
    """
    def get_coords_image(self, image : int) -> (float,float):
        return self.__fenetre.get_coords_image(image)

    """
    Change the color of the element
    """
    def change_color(self, element : int, color : str) -> None:
        self.__fenetre.change_color(element,color)

    """
    Add a bar chart to the window
    """
    def addBarChart(self, name : str) -> int:
        return self.__fenetre.addBarChart(name)

    """
    Set the color to the bar chart identified by id
    """
    def setColor(self, id : int, color : str) -> None:
        self.__fenetre.setColor(id, color)

    """
    Add a plot chart to the window
    """
    def addPlotChart(self, name : str) -> int:
        return self.__fenetre.addPlotChart(name)

    def addLimitedPlotChart(self, name : str, limit) -> int:
        return self.__fenetre.addLimitedPlotChart(name, limit)

    """
    Set the drawing policy to the curve of the plot chart identified by idCurve and id
    """
    def setPolicy(self, id : int, idCurve : int, policy : str) -> None:
        self.__fenetre.setPolicy(id, idCurve, policy)

    """
    Set the title to the chart identified by id
    """
    def setTitle(self, id : int, name : str) -> None:
        self.__fenetre.setTitle(id, name)

    """
    Set the label on the x axis to the chart identified by id
    """
    def setXLabel(self, id : int, name : str) -> None:
        self.__fenetre.setXLabel(id, name)

    """
    Set the label on the y axis to the chart identified by id
    """
    def setYLabel(self, id : int, name : str) -> None:
        self.__fenetre.setYLabel(id, name)

    """
    Add a curve to the plot with the given policy
    """
    def addCurve(self, id : int, policy : str) -> None:
        self.__fenetre.addCurve(id,policy)

    """
    Add a point to the plot with x,y coords
    """
    def addPoint(self, id : int, id_curve : int, x : float, y : float) -> None:
        self.__fenetre.addPoint(id,id_curve,x,y)

    """
    Add a column at the end of the figure
    """
    def addColumn(self, id : int, name : str) -> None:
        self.__fenetre.addColumn(id, name)

    """
    Remove the column chosen by its index
    """
    def removeColumn(self, id : int, index : int) -> None:
        self.__fenetre.removeColumn(id, index)

    """
    Set the column value chosen by its index
    """
    def setValue(self, id : int, index : int, value : float) -> None:
        self.__fenetre.setValue(id, index, value)

    """
    Increase the column value chosen by its index
    """
    def increaseValue(self, id : int, index : int, value : float) -> None:
        self.__fenetre.increaseValue(id, index, value)

    """
    Decrease the column value chosen by its index
    """
    def decreaseValue(self, id : int, index : int, value : float) -> None:
        self.__fenetre.decreaseValue(id, index, value)

    """
    Add an agent to amas
    """
    def updateAdd(self) -> None:
        print("Ajout d'un agent")

    """
    Remove an agent from amas
    """
    def updateRemove(self) -> None:
        print("Suppresion d'un agent")

    """
    Reset amas
    """
    def updateReset(self) -> None:
        print("Reset de la simulation")

    """
    Set the execution speed of amas
    """
    def updateScale(self, value : int) -> None:
        self.__scheduler.set_sleep(int(value))

    """
    Start or Stop the execution depending on the current state
    """
    def updateStartStop(self) -> None:
        if self.__is_run:
            self.__is_run = False
            self.__scheduler.stop()
        else:
            self.__is_run = True
            self.__scheduler.start()

    """
    Save the current state in the given file
    """
    def updateSave(self, filename : str) -> None:
        if filename != '':
            self.__scheduler.save(filename)

    def updateCycle(self) -> None:
        try:
            self.updateWindow()
        except:
            return

    def updateWindow(self) -> None:
        pass

    def initialisation(self) -> None:
        pass

    """
    Launch the scheduler in a thread and display the window
    """
    def start(self) -> None:
        self.initialisation()
        self.__th = Thread(target=self.__scheduler.run)
        self.__th.start()
        self.__fenetre.display()

    """
    Close the scheduler
    """
    def updateClosing(self) -> None:
        self.__scheduler.exit_program()


    """
    Display a message in the logs
    """
    def logsDisplay(self, message : str) -> None:
        self.__fenetre.logsDisplay(message)

    """
    Display an error in the logs
    """
    def errorDisplay(self, typeError : str, message : str)-> None:
        self.__fenetre.errorDisplay(typeError, message)
