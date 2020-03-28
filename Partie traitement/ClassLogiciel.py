# -*- coding: utf-8 -*-
class Logiciel:

    def __init__(self,nom):
        self.nom = nom
        self.heureDebut = "24:00:00"
        self.heureFin = ""
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
        self.heureDebut = ""
#        self.heureFin = ""
        self.infosComplementaires = ""

    def getType(self):
         return self.type

    def getHeureDebut(self):
         return self.heureDebut

#    def getHeureFin(self):
#         return self.heureFin

     def getInfoComplementaires(self):
          return self.infosComplementaires

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
