class Logiciel:
    
    def __init__(self,nom):
        self.nom = nom
        self.heureDebut = "24:00:00"
        self.listeActions = []
    
    def setHeureDebut(self):
        heurePlusPetite = "24:00:00"
        for action in self.listeActions:
            if self._heureToNb(action.heureDebut) < self._heureToNb(heurePlusPetite):
                heurePlusPetite = action.heureDebut
        self.heureDebut = heurePlusPetite

    
    def _heureToNb(self,heure):
        (h, m, s) = heure.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)    


#-------------------------------------------------------------------------

class Action:
    
    def __init__(self):
        self.type = ""
        self.heureDebut = ""
        self.infosComplementaires = ""
        
#--------------------------------------------------------------------------
    
class Session:
    def __init__(self):
        self.listeLogiciels = []
        self.heureDebut = ""
        self.heureFin = ""
        self.actionCount = ""
        
    def addLogiciel(self,logiciel):
        self.listeLogiciels.append(logiciel)
        
    def getNoms(self):
        tabNoms = []
        for logiciel in self.listeLogiciels:
            tabNoms.append(logiciel.nom)
        
        return tabNoms
        
