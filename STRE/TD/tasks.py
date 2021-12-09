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



        
