"""
Class Fenetre
"""

import os, sys
import pathlib
from tkinter.ttk import LabelFrame
from tkinter import ttk, Tk, PanedWindow, BOTTOM, Menu
from tkinter.filedialog import askopenfilename

sys.path.insert(0, str(pathlib.Path(__file__).parent))

from pyAmakIHM.classes.panelLogs import PanelLogs
from pyAmakIHM.classes.panelCommandes import PanelCommandes
from pyAmakIHM.classes.panelVue import PanelVue
from pyAmakIHM.classes.panelBarChart import PanelBarChart
from pyAmakIHM.classes.panelPlotChart import PanelPlotChart
from pyAmakIHM.classes.panelLimitedPlotChart import PanelLimitedPlotChart


class Fenetre :
    """
    Class Fenetre
    """

    def __init__(
            self,
            name: str
    ) -> None:

        self.__observer = None

        self.__images = []

        self.__root = Tk()

        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.__root.title(name)

        self.__root.geometry("1000x700")

        menubar = Menu(self.__root)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.notifyAboutSave)

        menubar.add_cascade(label="File", menu=filemenu)

        self.__root.config(menu=menubar)

        self.__panelCommandes = PanelCommandes(self.__root)

        self.__division = PanedWindow(self.__root, orient='vertical',showhandle = True,handlesize = 10)
        self.__division.pack(side='right', expand='yes', fill='both')

        self.__onglet = ttk.Notebook(self.__division)

        self.__onglet.bind('<ButtonPress>', self.drag_tab)

        self.__panelGraphiques = []

        self.__panelVue = PanelVue(self.__onglet)

        self.__onglet.add(self.__panelVue, text="Vue")

        self.__panel_log = PanelLogs(self.__division)

        self.__division.add(self.__onglet)

        self.__division.add(self.__panel_log)

    def get_root(self) -> Tk:
        return self.__root

    def get_canvas_width(self) -> float:
        return self.__panelVue.get_canvas_width()

    def get_canvas_height(self) -> float:
        return self.__panelVue.get_canvas_height()

    """
    Attach a observer to the object
    """
    def attach(self, observer : 'Controleur') -> None:
        self.__observer = observer
        self.__panelCommandes.attach(observer)

    """
    Draw a rectangle with x,y coords, height, width and color
    """
    def draw_rectangle(self, x : float, y : float, height : float, width : float, color : str) -> int:
        return self.__panelVue.draw_rectangle(x,y,height,width,color)

    """
    Draw a circle with x,y coords, radian and color
    """
    def draw_circle(self, x : float, y : float, radian : float, color : str) -> int:
        return self.__panelVue.draw_circle(x,y,radian,color)

    """
    Draw a line between x0,y0 and x1,y1 point with color
    """
    def draw_line(self, x0 : float, y0 : float, x1 : float, y1 : float, color : str) -> int:
        return self.__panelVue.draw_line(x0,y0,x1,y1,color)

    """
    Draw an image with x,y coords and its name
    """
    def draw_image(self, x : float, y : float, name : str) -> int:
        return self.__panelVue.draw_image(x,y,name)

    """
    Draw a text with x,y coords
    """
    def draw_text(self, x : float, y : float, text : str) -> int:
        return self.__panelVue.draw_text(x,y,text)

    """
    Move an image to x,y coords
    """
    def move_image(self, image : int, x : float, y : float) -> None:
        self.__panelVue.move_image(image, x, y)

    """
    Move an element to x,y coords
    """
    def move_element(self, element : int, x : float, y : float) -> None:
        self.__panelVue.move_element(element,x,y)

    """
    Remove an element
    """
    def remove_element(self, element : int) -> None:
        self.__panelVue.remove_element(element)

    """
    Remove all element
    """
    def remove_all(self) -> None:
        self.__panelVue.remove_all()

    """
    Give the element's coords
    """
    def get_coords_element(self, element : int) -> (float,float):
        return self.__panelVue.get_coords_element(element)

    """
    Give the image's coords
    """
    def get_coords_image(self, image : int) -> (float,float):
        return self.__panelVue.get_coords_image(image)

    """
    Change the color of the element
    """
    def change_color(self, element : int, color : str) -> None:
        self.__panelVue.change_color(element, color)

    """
    Add a bar chart to the window
    """
    def addBarChart(self, name : str) -> int:
        length = len(self.__panelGraphiques)
        self.__panelGraphiques.append(PanelBarChart(self.__onglet,length))

        self.__panelGraphiques[length].attach(self)
        self.__onglet.add(self.__panelGraphiques[length],text = name)
        return (length)

    """
    Set the color to the bar chart identified by id
    """
    def setColor(self, id : int, color : str) -> None:
        self.__panelGraphiques[id].setColor(color)

    """
    Add a plot chart to the window
    """
    def addPlotChart(self, name : str) -> int:
        length = len(self.__panelGraphiques)
        self.__panelGraphiques.append(PanelPlotChart(self.__onglet,length))

        self.__panelGraphiques[length].attach(self)
        self.__onglet.add(self.__panelGraphiques[length],text = name)
        return (length)

    def addLimitedPlotChart(self, name : str, limit) -> int:
        length = len(self.__panelGraphiques)
        self.__panelGraphiques.append(PanelLimitedPlotChart(self.__onglet,length, limit))

        self.__panelGraphiques[length].attach(self)
        self.__onglet.add(self.__panelGraphiques[length],text = name)
        return (length)


    """
    Set the drawing policy to the curve of the plot chart identified by idCurve and id
    """
    def setPolicy(self, id : int, idCurve, policy : str) -> None:
        self.__panelGraphiques[id].setPolicy(idCurve,policy)

    """
    Set the title to the chart identified by id
    """
    def setTitle(self, id : int, name : str) -> None:
        self.__panelGraphiques[id].setTitle(name)

    """
    Set the label on the x axis to the chart identified by id
    """
    def setXLabel(self, id : int, name : str) -> None:
        self.__panelGraphiques[id].setXLabel(name)

    """
    Set the label on the y axis to the chart identified by id
    """
    def setYLabel(self, id : int, name : str) -> None:
        self.__panelGraphiques[id].setYLabel(name)

    """
    Add a curve to the plot
    """
    def addCurve(self, id : int, policy : str) -> None:
        self.__panelGraphiques[id].addCurve(policy)

    """
    Add a point to the plot with x,y coords
    """
    def addPoint(self, id : int, id_curve : int, x : float, y : float) -> None:
        self.__panelGraphiques[id].addPoint(id_curve,x,y)

    """
    Add a column at the end of the figure
    """
    def addColumn(self, id : int, name : str) -> None:
        self.__panelGraphiques[id].addColumn(name)

    """
    Remove the column chosen by its index
    """
    def removeColumn(self, id : int, index : int) -> None:
        self.__panelGraphiques[id].removeColumn(index)

    """
    Set the column value chosen by its index
    """
    def setValue(self, id : int, index : int, value : float) -> None:
        self.__panelGraphiques[id].setValue(index, value)

    """
    Increase the column value chosen by its index
    """
    def increaseValue(self, id : int, index : int, value : float) -> None:
        self.__panelGraphiques[id].increaseValue(index, value)

    """
    Decrease the column value chosen by its index
    """
    def decreaseValue(self, id : int, index : int, value : float) -> None:
        self.__panelGraphiques[id].decreaseValue(index, value)

    """
    Bind the mouse's motion when a tab is dragged
    """
    def drag_tab(self, event : 'event') -> None:
        self.__onglet.bind('<B1-Motion>',self.is_drag)

    """
    Bind the mouse's button release when a tab is dragged
    """
    def is_drag(self, event : 'event') -> None:
        self.__root.config(cursor="fleur")
        self.__onglet.bind('<ButtonRelease>',self.tab_drop)

    """
    Create a copy in a window of the dragged tab
    """
    def tab_drop(self, event : 'event') -> None:
        self.__root.config(cursor="arrow")
        self.__onglet.unbind('<B1-Motion>')
        self.__onglet.unbind('<ButtonRelease>')

        tab_number = event.widget.index(event.widget.select())
        tab_name = event.widget.tab(event.widget.select(), 'text')

        if (tab_number >= 1):
            self.__onglet.hide(self.__panelGraphiques[tab_number-1])
            self.__panelGraphiques[tab_number-1] = self.__panelGraphiques[tab_number-1].createCopy(tab_name,tab_number-1)

    """
    Replace the 'Graphique' tab in the main window
    """
    def updateGraphique(self, panel : 'PanelGraphique', id : int) -> None:
        self.__panelGraphiques[id] = panel
        self.__onglet.add(self.__panelGraphiques[id])

    """
    Notify the controleur to stop the app and close the window
    """

    def on_closing(self) -> None:
        self.__observer.updateClosing()
        for pan in self.__panelGraphiques:
            pan.quit()
        self.__panelVue.quit()
        self.__panelCommandes.quit()
        self.__panel_log.quit()
        self.__root.quit()

    """
    Run the window application
    """
    def display(self) -> None:
        self.get_root().mainloop()

    def logsDisplay(self, message : str) -> None:
        self.__panel_log.logsDisplay(message)

    """
    Displaying logs on the screen
    """
    def errorDisplay(self,typeError : str, message : str) -> None:
        self.__panel_log.errorDisplay(typeError,message)

    """
    """
    def notifyAboutSave(self):
        fileName = askopenfilename(filetypes =[('Pickle Files', '*.pickle')])
        self.__observer.updateSave(fileName)
