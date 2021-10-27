"""
Class PanelCommandes
"""

from tkinter import IntVar, LabelFrame, Button, Scale, Label, Frame

class PanelCommandes(LabelFrame):
    """
    Class PanelCommandes
    """

    def __init__(
            self,
            root : 'Tk'
    ) -> None :

        self.__observer = None

        self.__compteur = IntVar(value=0)

        super().__init__(root,text='Commandes')
        self.pack(fill='both',side='left')

        bouttonStartStop = Button(self, text='start/stop',height=2,command=self.notifyObserverAboutStartStop)
        bouttonStartStop.pack(side='top',fill='x')

        frameBoutons = Frame(self)
        frameBoutons.pack(side='bottom',fill='x')

        frameBoutonAux = Frame(self)
        frameBoutonAux.pack(side='top')

        self.__slider = Scale(frameBoutons,orient='horizontal',from_=1,to=10,command=self.notifyObserverAboutScale)
        self.__slider.pack(side='bottom',fill='x')

        bouttonPlus = Button(frameBoutons,text='+',command=self.plus)
        bouttonPlus.pack(side='right')

        compteurLabel = Label(frameBoutons,textvariable=self.__compteur)
        compteurLabel.pack(side='right')

        bouttonMoins = Button(frameBoutons,text='-',command=self.moins)
        bouttonMoins.pack(side='right')

        bouttonReset = Button(frameBoutons,text='reset',command=self.notifyObserverAboutReset)
        bouttonReset.pack(side='right')

    """
    Attach a observer to the object
    """
    def attach(self, observer : 'Controleur') -> None:
        self.__observer = observer
        self.__slider.set(10)

    """
    Notify the observer that the Start.Stop button was pressed
    """
    def notifyObserverAboutStartStop(self) -> None:
        self.__observer.updateStartStop()

    """
    Notify the observer that the scale has change its value and give the current value
    """
    def notifyObserverAboutScale(self, value : int) -> None:
        sleep = 10/ int(value) - 1
        self.__observer.updateScale(sleep)

    """
    Notify the observer that the add button was pressed
    """
    def notifyObserverAboutAdd(self) -> None:
        self.__observer.updateAdd()

    """
    Notify the observer that the remove button was pressed
    """
    def notifyObserverAboutRemove(self) -> None:
        self.__observer.updateRemove()

    """
    Notify the observer that the reset button was pressed
    """
    def notifyObserverAboutReset(self) -> None:
        self.__observer.updateReset()

    """
    Add one to compteur and notify the observer
    """
    def plus(self) -> None:
        self.__compteur.set(self.__compteur.get()+1)
        self.notifyObserverAboutAdd()

    """
    Substract one to compteur and notify the observer except if compteur's value is zero
    """
    def moins(self) -> None:
        valeur = self.__compteur.get()
        if valeur > 0:
            self.__compteur.set(valeur-1)
            self.notifyObserverAboutRemove()
        else:
            self.__compteur.set(0)
