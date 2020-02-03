# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 19:03:22 2020
@author: Paul Lafourcade
"""
from lxml import etree
import csv #utilisation de la bibliothèque native csv

class Mot:
    def __init__(self):
        
        self.charInvisibles = ['Rshift', 'Lcontrol', 'Rcontrol', 'Lshift'] #Ces caractères ne seront pas affichés
        
        self.motFinal = ''
        self.heureDebut = None
        self.heureFin = None
       
        
    def ajouterLettre(self,lettre):
        """
        Ajoute une lettre au mot qui est en train d'etre créé, lettre est ajouté à la fin de motFinal
        """
        if lettre not in self.charInvisibles:
            if lettre == "Space":
                lettre = ' (Espace) '
            if lettre == "Return":
                lettre = ' (Entrée) '
            if lettre == "Back":
                lettre = ' (Retour) '  #Va falloir recoder tout le reste
            
            self.motFinal = self.motFinal + lettre
    
    def setHeureDebut(self,date):
        self.heureDebut = date
        
    def setHeureFin(self,date):
        self.heureFin = date
        
    def getMot(self):
        return self.motFinal
    
    def getHeureDebut(self):
        return self.heureDebut
    
    def getHeureFin(self):
        return self.heureFin
        

    


class BKLtoTxt:

    def __init__(self,nomFichier):
        
        self.nomFic = nomFichier
        
        # FIRST OU PAS
        self.first = False
        self.txtBool = False
        
        self.nouveauMot = None #contiendra le mot qui sera en train d'etre créé dans la boucle
        self.listeMots = []
    

    def recupererPhrases(self):
        
        """
        On parcours le tableau  entièrement afin d'en récupérer les suites de lettres qui formeront des phrases
        """
        
        with open(self.nomFic,encoding="utf8", errors='ignore') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t') #ouverture en tsv
        
            for row in reader:
                self.majStatutTexte(row[0])
                if self.isCurrentlyText() == True :
                    if self.isFirst() == True :
                        self.nouveauMot = Mot()
                        self.nouveauMot.setHeureDebut(row[6][13:])
                    self.nouveauMot.setHeureFin(row[6][13:])
                    self.nouveauMot.ajouterLettre(row[14])
                else :
                    if self.nouveauMot is not None:
                        self.listeMots.append(self.nouveauMot)
                        self.nouveauMot = None
                    
        return self.listeMots
    
    def majStatutTexte(self,lettre):
        '''
        permet de maj les booléens permettant de connaitre le statut actuel du texte
        '''
        if lettre == 'K':
            if self.txtBool == False:
                self.first = True
            else:
                self.first = False
            self.txtBool = True
        else:
            self.txtBool = False
            self.first = False
    
    def isCurrentlyText(self):
        return self.txtBool
    
    def isFirst(self):
        return self.first



