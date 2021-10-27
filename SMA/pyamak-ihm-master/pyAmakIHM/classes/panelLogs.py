"""
Class PanelLogs
"""

from tkinter import ttk, Scrollbar, PanedWindow, Text
import sys, subprocess , os, io
import contextlib
from tkinter.constants import INSERT

from pyAmakIHM.classes.panelCommandes import PanelCommandes


class PanelLogs(Text):
    """
    Class PanelLogs
    """

    def __init__(
            self,
            root : 'Tk'
    ) -> None :

        super().__init__(root,bg='white')

        self.__root = root

        """
        place where you can write and read logs
        """
        self.__affichage=Text(self)
        self.__affichage.pack(fill='both',expand='yes')


        """
        put scrollbars in the text place
        """
        self.__affichageScroll = Scrollbar(self.__affichage,orient="vertical",command=self.__affichage.yview)

        self.__affichage.configure(yscrollcommand=self.__affichageScroll.set)

        self.__affichageScroll.pack(side='right',fill='y')

    """
    return the logs place
    """
    def getText(self) -> Text :
        return self.__affichage


    """
    Display a message in the logs
    """
    def logsDisplay(self, message : str) -> None:
        place=self.getText()
        place.insert("end", message+"\n")
        place.see("end")

    """
    Display an error in the logs
    """
    def errorDisplay(self, typeError : str, message : str) -> None:
        self.logsDisplay("Erreur : "+typeError+", "+message)
        place.see("end")

