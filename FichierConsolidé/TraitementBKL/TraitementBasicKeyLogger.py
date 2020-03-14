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
        
    

   #remarque: demande encore toute une série de test avant d'etre classé comme opérationnel


class GestionBKL:

    def __init__(self,nomFichier):
        
        self.nomFic = nomFichier
        
        # FIRST OU PAS
        self.first = False
        self.txtBool = False
        
        self.nouveauMot = None #contiendra le mot qui sera en train d'etre créé dans la boucle
        self.listeMots = []
    

    def __recupererPhrases(self):
        
        """
        On parcours le tableau  entièrement afin d'en récupérer les suites de lettres qui formeront des phrases
        """
        
        with open(self.nomFic,encoding="utf8", errors='ignore') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t') #ouverture en tsv
        
            for row in reader:
                self.__majStatutTexte(row[0])
                if self.__isCurrentlyText() == True :
                    if self.__isFirst() == True :
                        self.nouveauMot = Mot()
                        self.nouveauMot.setHeureDebut(row[6][13:])
                    self.nouveauMot.setHeureFin(row[6][13:])
                    self.nouveauMot.ajouterLettre(row[14])
                else :
                    if self.nouveauMot is not None:
                        self.listeMots.append(self.nouveauMot)
                        self.nouveauMot = None
    
    def __heureToNb(self,heure): #string sous forme de date en nb
        (h, m, s) = heure.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)    
         

       
    def ajoutDuBKLaPSR(self,nomFichierPSR, nomNouveauFichierXML):
        """
            Seule fonction a lancer
        """
        
        self.listeMots = self.__recupererPhrases()
        
        #initialisation du xml
        tree = etree.parse(nomFichierPSR) 
        root = tree.getroot()
        etree.tostring(root)
        
        for texteAction in root.xpath('/Report/UserActionData/RecordSession/EachAction/Action/text()'):
            if texteAction == "Saisie au clavier":
                self.__traitementDeUnePhrase(root, texteAction)
                        
        #enregistrement de l'xml modifié
        etree.ElementTree(root).write(nomNouveauFichierXML, pretty_print = True, xml_declaration=True, encoding="utf-8")
    
    
    
    def __traitementDeUnePhrase(self,root, texteAction):
        parent = texteAction.getparent().getparent() #Balise EachAction de l'action récupérée

        action = texteAction.getparent() #Balise action en elle meme
        
        #temp de debut de l'action et fin (debut de la suivante)
        debutActionPSR = parent.get("Time")
        parentSuivant = parent.getnext()
        nextActionPSR = parentSuivant.get("Time")
        
        
        for mot in self.listeMots:
            if (self.__heureToNb(mot.getHeureDebut()) >= self.__heureToNb(debutActionPSR) and (self.__heureToNb(mot.getHeureFin()) <= self.__heureToNb(nextActionPSR))):
                
                #creation de l'element de texte
                baliseTxt = etree.Element("texte")
                baliseTxt.set("heureDebut", mot.getHeureDebut())
                baliseTxt.set("heureFin", mot.getHeureFin())
                baliseTxt.text = mot.getMot()

                parent.insert(parent.index(action)+1, baliseTxt) #insertion après l'action
    
        
    
    def __majStatutTexte(self,lettre):
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
    
    def __isCurrentlyText(self):
        return self.txtBool
    
    def __isFirst(self):
        return self.first

