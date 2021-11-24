
class Communication():
    


  
    def __init__(self):
        self._contacts = []
        self._BAL = []


    def ajouterContact(self,c):
        self._contacts.append(c)
        print(self._contacts)

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

    def getContacts(self):
        return self._contacts

    
