from pyAmakCore.classes.tools.schedulerIHM import SchedulerIHM

from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy
from pyAmakCore.exception.override import ToOverrideWarning
from pyAmakIHM.classes.fenetre import Fenetre
from controleurPhilosophersExample import ControleurPhilosophersExample
from philosophersAmasExample import PhilosophersAmasExamples

fenetre = Fenetre("Prototype Philosophers")

ToOverrideWarning.enable_warning(False)

amas = PhilosophersAmasExamples(ExecutionPolicy.ONE_PHASE)

scheduler = SchedulerIHM(amas)

controleur = ControleurPhilosophersExample(fenetre, scheduler)


def main():
    controleur.start()


main()
