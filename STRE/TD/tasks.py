# Task module

class Task():
    def __init__(self, name, idx, period, deadline, wcet):
        self.name=name
        self.idx=idx
        self.period=period
        self.deadline=deadline
        self.wcet=wcet

    def __str__(self):
        s = "Task: "+str(self.idx)+ "\n\tname = "+self.name+ "\n\tperiod = "+str(self.period) + "\n\tdeadline = "+str(self.deadline)+"\n\tduration = "+str(self.wcet)+ "\n"
        return s

    def is_my_time(self, time):
        if( (time % self.period) == 0 ):
            return True
        return False


def get_tasks_to_add(time, tasks):
    tasksToAdd = []
    for t in tasks:
        if t.is_my_time(time):
            tasksToAdd.append([t, t.wcet])
    
    return tasksToAdd
        
