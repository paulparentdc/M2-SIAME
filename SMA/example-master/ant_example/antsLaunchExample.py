"""
Class antsLaunchExample
"""
import sys
sys.path.extend({"/nfs/home/camsi8/Documents/M2-SIAME/SMA/pyamak-core","/nfs/home/camsi8/Documents/M2-SIAME/SMA/pyamak-ihm-master"})
from random import seed
from time import sleep

from pyAmakCore.classes.tools.schedulerIHM import SchedulerIHM
from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy

from pyAmakIHM.classes.fenetre import Fenetre
from controleurAntsExample import ControleurAntsExample
from worldExample import WorldExample
from antHillExample import *

from pyAmakCore.exception.override import ToOverrideWarning


class SimpleScheduler(SchedulerIHM):

    def last_part(self):
        super().last_part()
        if self.amas.get_cycle() == 100:
            self.save()
            sleep(10)
            self.exit_program()


seed()

ToOverrideWarning.enable_warning(False)

fenetre = Fenetre("Prototype Ants")


"""
env = WorldExample(0, fenetre.get_canvas_width(), 0, fenetre.get_canvas_height(), 5, 7)
# amas = AntHillExample(env, ExecutionPolicy.ONE_PHASE)
amas = AntHillExample(env, ExecutionPolicy.TWO_PHASES)

scheduler = SimpleScheduler(amas)
"""
scheduler = SimpleScheduler.load()

controleur = ControleurAntsExample(fenetre, scheduler)
def main():
    controleur.start()


main()
