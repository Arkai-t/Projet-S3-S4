import datetime

class Action:
    
    def __init__(self):
        self.nom = ""
        self.type = ""
        self.description = ""
        self.heureDebut = ""
        self.nomPage = ""
      
   
    def setDescription(self, desc):
        self.description = desc
        
    def getType(self):
         return self.type

    def getHeureDebut(self):
         return self.heureDebut   
     
    def setNomPageFromUIAStack(self, balise):
        levels = balise.getchildren()
        for level in levels: #parcours de toutes les balises level   any('Name' in attr[0] for attr in levelAttributs
            levelAttributs = level.items()
            if self.nomPage == "":
                for i, attribut in enumerate(levelAttributs):
                    if attribut[0] == "LocalizedControlType" and attribut[1] == "fenêtre":
                        self.nomPage = levelAttributs[i-1][1] 
    def getNom(self):
         return self.nom

    def getType(self):
         return self.type

    def getDescription(self):
         return self.description

    def getHeureDebut(self):
         return self.heureDebut

    def getNomPage(self):
         return self.nomPage                    
        
     

class ActionClic(Action):
    def __init__(self):
        Action.__init__(self)
        
    def setType(self, typeAction):
        self.type = typeAction
    def setNom(self):
        self.nom = "Clic"
        



class ActionSaisie(Action):
    def __init__(self):
        Action.__init__(self)
        self.phrase = ""
        
    def setType(self, typeAction):
        self.type = typeAction
        
    def setNom(self):
        self.nom = "Saisie"  
        
    def getPhrase(self):
         return self.phrase    
        


class ActionEnregistrer(Action):
    def __init__(self):
        Action.__init__(self)

    def setType(self, typeAction):
        self.type = "Enregistrement"
    def setNom(self):
        self.nom = "Enregistrement"    
    
class ActionCompiler(Action):
    def __init__(self):
        Action.__init__(self)
        
    def setType(self, typeAction):
        self.type = "Compilation"
    def setNom(self):
        self.nom = "Compilation"  
        

#-------------------------------------------------------------------------

class Logiciel:
    
    def __init__(self,nom):
        self.nom = nom
        self.heureDebut = "24:00:00"
        self.listeActions = []
        self.tempsPasse = "00:00:00"
    
    def setHeureDebut(self):
        heurePlusPetite = "24:00:00"
        for action in self.listeActions:
            if self._heureToNb(action.heureDebut) < self._heureToNb(heurePlusPetite):
                heurePlusPetite = action.heureDebut
        self.heureDebut = heurePlusPetite
        
    def addAction(self, action, temps):
        self.listeActions.append(action)
        secondesPassees = self._heureToNb(self.tempsPasse)
        secondesPassees += temps
        self.tempsPasse = str(datetime.timedelta(seconds=secondesPassees)) #convertir les secondes en HH:MM:SS
        
        
    
    def _heureToNb(self,heure):
        (h, m, s) = heure.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)  
    
    #def _secToHeure(self,secondes):
        
    
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
