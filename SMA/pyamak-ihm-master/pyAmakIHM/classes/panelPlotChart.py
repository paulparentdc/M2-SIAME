"""
Class PanelPlotChart
"""

from tkinter import Frame, Toplevel
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PanelPlotChart(Frame):
    """
    Class PanelPlotChart
    """

    def __init__(
            self,
            root : 'Tk',
            id : int
    ) -> None :

        super().__init__(root)

        self.__root = root
        self.__fig = Figure()

        self._axis = self.__fig.add_subplot()
        self._xAxis = [[]]
        self._yAxis = [[]]

        self._axis.plot(self._xAxis,self._yAxis)

        self.__graphique = FigureCanvasTkAgg(self.__fig,master = self)
        self.__graphique.get_tk_widget().pack(fill='both',expand='yes')

        self.__title = ''
        self.__XLabel = ''
        self.__YLabel = ''
        self.__policy = ['bo-']

        self.__id = id

        self._copy = None
        self._observer = None

    """
    Attach a observer to the object
    """
    def attach(self, obs : 'Fenetre') -> None:
        self._observer = obs

    """
    Notify the observer about an event
    """
    def notify(self, panel : 'PanelBarChart', id : int) -> None:
        self._observer.updateGraphique(panel,id)

    """
    Set the drawing policy for the curve identified by idCurve
    """
    def setPolicy(self, idCurve : int, policy : str) -> None:
        self._axis.clear()
        self.__policy[idCurve] = policy
        self._rebuild()

    """
    Set the title to the chart
    """
    def setTitle(self, name : str) -> None:
        self._axis.clear()
        self.__title = name
        self._rebuild()

    """
    Set the label on the x axis to the chart
    """
    def setXLabel(self, name : str) -> None:
        self._axis.clear()
        self.__XLabel = name
        self._rebuild()

    """
    Set the label on the y axis to the chart
    """
    def setYLabel(self, name : str) -> None:
        self._axis.clear()
        self.__YLabel = name
        self._rebuild()

    """
    Add a curve to the plot with the given policy
    """
    def addCurve(self, policy : str) -> None:
        self._xAxis.append([])
        self._yAxis.append([])
        self.__policy.append(policy)


    """
    Add a point to the id curve with x,y coords
    """
    def addPoint(self, id : int, x : int, y : int):
        self._axis.clear()
        self._xAxis[id].append(x)
        self._yAxis[id].append(y)

        self._rebuild()

    """
    Rebuild the figure after any modification
    """
    def _rebuild(self) -> None:
        for i in range (len(self._xAxis)):
            self._axis.plot(self._xAxis[i],self._yAxis[i],self.__policy[i])

        self._axis.title.set_text(self.__title)
        self._axis.set_xlabel(self.__XLabel)
        self._axis.set_ylabel(self.__YLabel)
        self.__graphique.draw()

    """
    Return a copy of the object
    """
    def createCopy(self, name : str, id : int) -> 'PanelPlotChart':
        window = Toplevel()
        window.title(name)

        self._copy = PanelPlotChart(window, id)
        self._copy.pack(fill='both',expand='yes')

        self._copyWidget()

        self._copy._rebuild()

        self._copy._copy = self
        self._copy._observer = self._observer

        window.protocol("WM_DELETE_WINDOW", self._copy.on_closing)
        window.geometry("+900+0")

        return self._copy

    """
    Copy the object
    """
    def _copyWidget(self) -> None:
        self._copy.__id = self.__id
        self._copy.__policy = self.__policy
        self._copy._xAxis = self._xAxis
        self._copy._yAxis = self._yAxis
        self._copy.__title = self.__title
        self._copy.__XLabel = self.__XLabel
        self._copy.__YLabel = self.__YLabel

    """
    Send the original object to the main window when the window is closing
    """
    def on_closing(self) -> None:
        self._copyWidget()
        self._copy._rebuild()
        self.__root.destroy()
        self.notify(self._copy, self._copy.__id)
