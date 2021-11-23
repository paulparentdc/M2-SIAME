
class Communication():
    _BAL = []
    _contacts = []


    def ajouterContact(self,c):
        self._contacts.append(c)

    def razBAL(self):
        while(self._BAL):
            self._BAL.pop()

    def sendMsg(self, message):
        for c in self._contacts :
            c.receiveMsg(message)
        
    def receiveMsg(self, message):
        self._BAL.append(message)

    def getBAL(self):
        return self._BAL

    
