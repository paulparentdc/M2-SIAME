from pyAmakCore.classes.scheduler_mono_threading import SchedulerMono

from pyAmakCore.exception.override import ToOverrideWarning
from pyAmakCore.classes.agent import Agent
from pyAmakCore.classes.amas import Amas
from pyAmakCore.classes.environment import Environment
from pyAmakCore.classes.scheduler import Scheduler


class SimpleAgent(Agent):
    pass


class SimpleAmas(Amas):
    def on_initialization(self) -> None:
        # self.set_do_log(True)
        pass

    def on_initial_agents_creation(self) -> None:
        for i in range(10):
            self.add_agent(SimpleAgent(self))

class SimpleEnv(Environment):
    pass

class SimpleSchedulerMono(SchedulerMono):

    def last_part(self) -> None:
        super().last_part()
        self.save("test.pickle")

import time
start_time = time.time()
ToOverrideWarning.enable_warning(False)

env = SimpleEnv()
amas = SimpleAmas(env)

#scheduler = Scheduler(amas)
scheduler = SimpleSchedulerMono(amas)

scheduler.start()
scheduler.run()
print("--- %s seconds ---" % (time.time() - start_time))


"""
There are no visible memory leak in pyAmakCore
TODO : 
We could test add agent / get most critical neighbor ... also
"""
