"""
Class PanelBarChart
"""

from tkinter import Frame, Toplevel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PanelBarChart(Frame):
    """
    Class PanelBarChart
    """

    def __init__(
            self,
            root : 'Tk',
            id : int
    ) -> None :

        super().__init__(root)

        self.__root = root
        self.__fig = Figure()

        self.__axis = self.__fig.add_subplot()
        self.__xAxis = []
        self.__yAxis = []

        self.__axis.bar(self.__xAxis,self.__yAxis)

        self.__graphique = FigureCanvasTkAgg(self.__fig,master = self)
        self.__graphique.get_tk_widget().pack(fill='both',expand='yes')

        self.__title = ''
        self.__XLabel = ''
        self.__YLabel = ''
        self.__color = 'tab:blue'

        self.__id = id

        self.__copy = None
        self.__observer = None

    """
    Attach a observer to the object
    """
    def attach(self, obs : 'Fenetre') -> None:
        self.__observer = obs

    """
    Notify the observer about an event
    """
    def notify(self, panel : 'PanelBarChart', id : int) -> None:
        self.__observer.updateGraphique(panel,id)

    """
    Set the color to the bar chart
    """
    def setColor(self, color : str) -> None:
        self.__axis.clear()
        self.__color = color
        self.__rebuild()

    """
    Set the title to the chart
    """
    def setTitle(self, name : str) -> None:
        self.__axis.clear()
        self.__title = name
        self.__rebuild()

    """
    Set the label on the x axis to the chart
    """
    def setXLabel(self, name : str) -> None:
        self.__axis.clear()
        self.__XLabel = name
        self.__rebuild()

    """
    Set the label on the y axis to the chart
    """
    def setYLabel(self, name : str) -> None:
        self.__axis.clear()
        self.__YLabel = name
        self.__rebuild()

    """
    Add a column at the end of the figure
    """
    def addColumn(self, name : str) -> None:
        self.__axis.clear()
        self.__xAxis.append(name)
        self.__yAxis.append(0)
        self.__rebuild()

    """
    Remove the column chosen by its index
    """
    def removeColumn(self, index : int) -> None:
        self.__axis.clear()
        del self.__xAxis[index]
        del self.__yAxis[index]
        self.__rebuild()

    """
    Set the column value chosen by its index
    """
    def setValue(self, index : int, value : float) -> None:
        self.__axis.clear()
        self.__yAxis[index] = value
        self.__rebuild()

    """
    Increase the column value chosen by its index
    """
    def increaseValue(self, index : int, value : float) -> None:
        self.__axis.clear()
        self.__yAxis[index] += value
        self.__rebuild()

    """
    Decrease the column value chosen by its index
    """
    def decreaseValue(self, index : int, value : float) -> None:
        self.__axis.clear()
        self.__yAxis[index] -= value
        self.__rebuild()

    """
    Rebuild the figure after any modification
    """
    def __rebuild(self) -> None:
        self.__axis.bar(self.__xAxis,self.__yAxis,color=self.__color)
        self.__axis.title.set_text(self.__title)
        self.__axis.set_xlabel(self.__XLabel)
        self.__axis.set_ylabel(self.__YLabel)
        self.__graphique.draw()

    """
    Return a copy of the object
    """
    def createCopy(self, name : str, id : int) -> 'PanelBarChart':
        window = Toplevel()
        window.title(name)

        self.__copy = PanelBarChart(window, id)
        self.__copy.pack(fill='both',expand='yes')

        self.__copyWidget()

        self.__copy.__rebuild()

        self.__copy.__copy = self
        self.__copy.__observer = self.__observer

        window.protocol("WM_DELETE_WINDOW", self.__copy.on_closing)
        window.geometry("+900+0")

        return self.__copy

    """
    Copy the object
    """
    def __copyWidget(self) -> None:
        self.__copy.__id = self.__id
        self.__copy.__xAxis = self.__xAxis
        self.__copy.__yAxis = self.__yAxis
        self.__copy.__title = self.__title
        self.__copy.__XLabel = self.__XLabel
        self.__copy.__YLabel = self.__YLabel

    """
    Send the original object to the main window when the window is closing
    """
    def on_closing(self) -> None:
        self.__copyWidget()
        self.__copy.__rebuild()
        self.__root.destroy()
        self.notify(self.__copy, self.__copy.__id)
