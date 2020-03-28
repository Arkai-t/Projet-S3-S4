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
    
    def getNom(self):
         return self.nom

    def getHeureDebut(self):
         return self.heureDebut

    def getHeureFin(self):
         return self.heureFin

    def getActions(self):
         return self.listeActions



#-------------------------------------------------------------------------

class Action:
    
    def __init__(self):
        self.type = ""
        self.description = ""
        self.heureDebut = ""
        self.localisationAction = ""
        self.nomPage = ""
        self.mots = []
        
    def addMot(self,mot,dateDebut,dateFin):
        if self.type == "Saisie au clavier":
            self.mots.append([mot,dateDebut,dateFin])
            
    def getType(self):
         return self.type

    def getHeureDebut(self):
         return self.heureDebut
     
    def getLocalisationAction(self):
         return self.localisationAction
     
    def getNomPage(self):
         return self.nomPage
     
    def getMots(self):
        return self.mots
    
        
        
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
            
    def getHeureDebut(self):
         return self.heureDebut

    def getHeureFin(self):
         return self.heureFin

    def getLogiciels(self):
         return self.listeLogiciels
        
        
