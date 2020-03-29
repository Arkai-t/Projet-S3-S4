class Logiciel:
    
    def __init__(self,nom):
        self.nom = nom
        self.heureDebut = "24:00:00"
        self.listeActions = []
        self.tempsPasse = ""
    
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
     
    def getTempsPasse(self):
         return self.tempsPasse



#-------------------------------------------------------------------------

class Action:
    
    def __init__(self):
        self.type = ""
        self.description = ""
        self.heureDebut = ""
        self.nomPage = ""
   
    def setDescription(self, desc):
        self.description = desc
     

class ActionClic(Action):
    def __init__(self):
        Action.__init__(self)
        
    def setType(self, type):
        self.type = type



class ActionSaisie(Action):
    def __init__(self):
        Action.__init__(self)
        self.phrase = ""
        
    def setType(self, type):
        self.type = type


class ActionEnregistrer(Action):
    def __init__(self):
        Action.__init__(self)

    def setType(self, type):
        self.type = "Enregistrement"
    
class ActionCompiler(Action):
    def __init__(self):
        Action.__init__(self)
        
    def setType(self, type):
        self.type = "Compilation"
        
        
#--------------------------------------------------------------------------
    
class Session:
    def __init__(self):
        self.listeLogiciels = []
        self.heureDebut = ""
        self.heureFin = ""
        
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
        
        
