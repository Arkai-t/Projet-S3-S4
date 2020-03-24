class Logiciel:
    
    def __init__(self,nom):
        self.nom = nom
        self.heureDebut = ""
        self.heureFin = ""
        self.listeAction = []
        
    def addAction(self,action):
        self.listeAction.append(action)
    
    def setHeures(self): #Récupère l'heure min et max et les met dans heureDebut et heureFin
        self.heureDebut = self.listeAction[0].heureDebut
        for action in self.listeAction:
            if self._heureToNb(action.heureDebut) < self._heureToNb(self.heureDebut):
                self.heureDebut = action.heureDebut
            if self._heureToNb(action.heureFin) < self._heureToNb(self.heureFin):
                self.heureFin = action.heureFin
    def _heureToNb(self,heure):
        (h, m, s) = heure.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)    

class Action:
    
    def __init__(self):
        self.type = ""
        self.heureDebut = ""
        self.heureFin = ""
        self.infosComplementaires = ""
        
    
    
    
        
