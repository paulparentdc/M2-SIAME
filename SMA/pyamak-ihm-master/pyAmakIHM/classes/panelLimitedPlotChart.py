"""
Class PanelLimitedPlotChart
"""

from pyAmakIHM.classes.panelPlotChart import PanelPlotChart
from tkinter import Toplevel

class PanelLimitedPlotChart(PanelPlotChart):
    """
    Class PanelLimitedPlotChart
    """

    def __init__(
            self,
            root : 'Tk',
            id : int,
            limit : int
    ) -> None :
        super().__init__(root, id)

        self.__limit = limit
        self.__limited = False

    """
    Add a point to the id curve with x,y coords
    """
    def addPoint(self, id : int, x : int, y : int) -> None:
        self._axis.clear()
        self._xAxis[id].append(x)
        self._yAxis[id].append(y)

        if(self.__limited):
            del self._xAxis[id][0]
            del self._yAxis[id][0]

        else:
            self.__limited = self.isLimited(id)

        self._rebuild()

    """
    Return true if number of points is over the limit
    """
    def isLimited(self,id : int) -> bool:
        return len(self._xAxis[id]) > self.__limit

    """
    Return a copy of the object
    """
    def createCopy(self, name : str, id : int) -> 'PanelLimitedPlotChart':
        window = Toplevel()
        window.title(name)

        self._copy = PanelLimitedPlotChart(window, id, self.__limit)
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
        super()._copyWidget()
        self._copy.__limit = self.__limit
        self._copy.__limited = self.__limited
