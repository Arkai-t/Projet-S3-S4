# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:53:41 2020
@author: Louison VINCENT, Paul LAFOURCADE, Malo LE MESTRE
"""

from os import remove
from datetime import timedelta
from lxml import etree
from json import load
from shutil import move
from ClassLogiciel import Session, Logiciel, Action, ActionEnregistrer, ActionCompiler, ActionClic, ActionSaisie

"""
Chemins des paramètres du projet
"""
pathConfig = r".\Config_traitement.json"

class FichierConsolide:
    """
    Classe qui permet l'écriture d'un fichier consolidé
    Pour l'instant elle ne se préocupe pas que :
        - les valeurs passées aux fonctions sont au bon format (string)
        - les valeurs soient cohérentes (une action d'un logiciel peut se produire
          en dehors de la période d'utilisation du logiciel)
        - de l'effacement de valeurs'
    """

    def __init__(self):
        """
        Définit la racine du fichier consolidé et les informations concernant les traces
        """
        #Création de la racine
        self.root = etree.Element("Session")
        self.sessionTP = Session()

    def creerArborescence(self):
        heureDebut = etree.SubElement(self.root, "HeureDebut")
        heureDebut.text = self.sessionTP.getHeureDebut()

        heureFin = etree.SubElement(self.root, "HeureFin")
        heureFin.text = self.sessionTP.getHeureFin()

        logiciels = etree.SubElement(self.root, "Logiciels")
        #Parcourir les logiciels
        for logicielCourant in self.sessionTP.getLogiciels():
             #Créer un logiciel
             logiciel = etree.SubElement(logiciels, "Logiciel")
             logiciel.set("nom", logicielCourant.getNom())

             heureDebutLogiciel = etree.SubElement(logiciel, "HeureDebut")
             heureDebutLogiciel.text = logicielCourant.getHeureDebut()

             tempsPasse = etree.SubElement(logiciel, "TempsPasse") 
             tempsPasse.text = logicielCourant.getTempsPasse()

             actions = etree.SubElement(logiciel, "Actions")
             #Parcourir les actions
             for actionCourante in logicielCourant.getActions():
                  action = etree.SubElement(actions, "Action")
                  action.set("nom", actionCourante.getNom())

                  typeAction = etree.SubElement(action, "TypeAction")
                  typeAction.text = actionCourante.getType()

                  description = etree.SubElement(action, "Description")
                  description.text = actionCourante.getDescription()

                  heureDebut = etree.SubElement(action, "HeureDebut")
                  heureDebut.text = actionCourante.getHeureDebut()

                  nomPage = etree.SubElement(action, "NomPage")
                  nomPage.text = actionCourante.getNomPage()

                  if isinstance(actionCourante, ActionSaisie):
                       saisie = etree.SubElement(action, "Saisie")
                       saisie.text = actionCourante.getPhrase()

    def sauvegardeFichier(self):
        """
        Permet la sauvegarde de l'arborescence créée dans un fichier
        """
        #Récupérer la configuration dans pathConfig
        file = open(pathConfig, encoding='utf-8')
        data = load(file)
        file.close()

        #Créer le fichier
        nomFic = (data["parametres"]["nomFic"] + "_FichierConsolide.xml")
        etree.ElementTree(self.root).write(nomFic, pretty_print = True, xml_declaration=True, encoding="utf-8")

        #Deplacer fichier dans StockageFichier
        move(nomFic, data["repertoireStockageFichiers"] + '\\' + nomFic)
        
        #Supprimer le fichier fusionné
        self.__supprimerFichierFusionne(data["repertoireStockageFichiers"] + "\\" + data["parametres"]["nomFic"] + "_FichierFusionne.xml")
        
    def recupererInformations(self):
        """
        Permet de récupérer les informations du ficher 
        """
        
        #Recuperer dans le Config_traitements.json
        file = open(pathConfig, encoding='utf-8')
        data = load(file)
        file.close()

        fichier = data["repertoireStockageFichiers"] + '\\' + data["parametres"]["nomFic"] + "_FichierFusionne.xml"
        

        #ouverture du xml        
        tree = etree.parse(fichier)
        
        #infos de session
        session = tree.xpath("/Report/UserActionData/RecordSession")
        attrSession = session[0].items() #récupérer tous les attributs de la balsie recordsession         
        
        self.sessionTP.heureDebut = self.__getSpecificAttribute(session[0],"StartTime")
        self.sessionTP.heureFin = self.__getSpecificAttribute(session[0],"StopTime")
        
        listeEachActions = session[0].getchildren()
        
        for i,action in enumerate(listeEachActions): #chaque action: (enumerate permet de compter le nombre de tours du for et de le mettre dans i)
            
            attributsActions = action.items() # .items renvoie les attributs sous forme de [[nom, valeur],[nom, valeur],[nom, valeur]]
            
            #get nom et creation du logiciel
            nomLogiciel = self.__getSpecificAttribute(action, "FileDescription")
            heureAction = self.__getSpecificAttribute(action, "Time")
            nouveauLogiciel = Logiciel(nomLogiciel)
            
            #remplir les actions 
            balisesDeEachAction = action.getchildren()
            
            isActionSpeciale = False #permettra de savoir si c'est un clic normal ou spécial (sauvegarde, compilation)
            
            baliseAction = self.__getSpecificChild(action,"Action")
            typeAction = baliseAction.text.split(" ",1)[0] #Recupérer premier mot du texte de la balise Action
            if typeAction == "Clic": #Savoir si c'est clic
                #Savoir de quel type d'action de clic est l'action
                UIAStack = self.__getSpecificChild(action, "UIAStack")
                for level in UIAStack.getchildren(): #Chaque balise level contenu dans la balise UIAStack
                    for attribut in level.items():  #chaque attributs de la balise level
                        if attribut[0] == "Name": #chercher si il y a un nom
                            if self.__isEnregistrer(attribut[1]): 
                                nouvelleAction = ActionEnregistrer()
                                isActionSpeciale = True
                                break
                            if self.__isCompiler(attribut[1]):
                                nouvelleAction = ActionCompiler()
                                isActionSpeciale = True
                                break
                    
                if isActionSpeciale == False:
                    nouvelleAction = ActionClic()          
                    
                #Remplir
                balise = self.__getSpecificChild(action,"Action")
                nouvelleAction.setType(balise.text)
                balise = self.__getSpecificChild(action,"Description")        
                nouvelleAction.description = balise.text
                balise = self.__getSpecificChild(action,"UIAStack")
                #Traitement du UIAStack
                nouvelleAction.setNomPageFromUIAStack(balise)
                
                nouvelleAction.heureDebut = heureAction
                nouvelleAction.setNom() #setNom met a jour le nom autaumatiquement selon quel type de clic nouvelleAction est
                if i != 0: #Si on est pas dans le premier tour (on va chercher l'heure de l'action précédente donc pour la première action il n'y a pas d'action précédente
                    nouveauLogiciel.addAction(nouvelleAction,self.__heureToNb(heureAction)-self.__heureToNb(self.__getSpecificAttribute(action.getprevious(),"Time"))) #self.__heureToNb(heureAction)-self.__heureToNb(self.__getSpecificAttribute(action.getprevious(),"Time")) permet de récupérer le temps passé sur l'action en faisant temps de l'action - temps de l'action précédente
                else:
                    nouveauLogiciel.listeActions.append(nouvelleAction)
                nouveauLogiciel.setHeureDebut() #cherche l'heureDebut min en cherchant dans toutes les actions du logiciel
                
            #Si c'est un texte
            if typeAction == "Saisie":
                for baliseTexte in balisesDeEachAction: #On utilise pas getSpecificChild car il peut y avoir plusieurs balises texte
                    if baliseTexte.tag == "texte":
                        #Création et remplissage de l'actionSaisie
                        nouvelleAction = ActionSaisie()
                        attributsTextes = baliseTexte.items()
                        balise = self.__getSpecificChild(action,"Action")
                        nouvelleAction.setType(balise.text)
                        balise = self.__getSpecificChild(action,"Description")        
                        nouvelleAction.description = balise.text
                        balise = self.__getSpecificChild(action,"UIAStack")
                        #Traitement du UIAStack
                        nouvelleAction.setNomPageFromUIAStack(balise)
                        
                        nouvelleAction.heureDebut = attributsTextes[0][1]  #heure de debut de l'action
                        nouvelleAction.phrase = baliseTexte.text
                        nouvelleAction.setNom()
                        if i != 0: #Meme commentaire qu'au dessus (meme code)
                            nouveauLogiciel.addAction(nouvelleAction,self.__heureToNb(heureAction)-self.__heureToNb(self.__getSpecificAttribute(action.getprevious(),"Time")))
                        else:
                            nouveauLogiciel.listeActions.append(nouvelleAction)
                        nouveauLogiciel.setHeureDebut()
                        
                        
                        
                        #Determiner si c'est un enregistrement en cherchant "CTRL-S" dans la chaine de caracteres
                        if len(str(baliseTexte.text)) > 0: #non vide
                            if "Ctrl+S" in baliseTexte.text:
                                
                                nouvelleActionEnregistrer = ActionEnregistrer()
                                nouvelleActionEnregistrer.setType("Enregistrement") #Sera set grace à l'héritage à Enregistrement quoi que ce soit
                                nouvelleActionEnregistrer.setDescription("L'utilisateur a enregistré en appuyant sur Ctrl+S")
                                nouvelleActionEnregistrer.heureDebut = attributsTextes[0][1]
                                balise = self.__getSpecificChild(action,"UIAStack")
            
                                #Traitement du UIAStack
                                nouvelleActionEnregistrer.setNomPageFromUIAStack(balise)
                                                        
                                nouvelleActionEnregistrer.setNom()                    
                                nouveauLogiciel.listeActions.append(nouvelleActionEnregistrer)
                                nouveauLogiciel.setHeureDebut()
        
            #ajout (ou modif du logiciel)
            if (self.sessionTP.listeLogiciels): #si sessionTP.listeLogiciels non vide
                if(nouveauLogiciel.nom in self.sessionTP.getNoms()): #si logiciel existe déjà
                    #Ajouter les actions de nouveauLogiciel au logiciel déjà présent dans listeLogiciels
                    for logiciel in self.sessionTP.listeLogiciels:
                        if logiciel.nom == nomLogiciel:
                            logiciel.setHeureDebut()
                            logiciel.listeActions += nouveauLogiciel.listeActions
                            logiciel.tempsPasse = str(timedelta(seconds=   (  self.__heureToNb(logiciel.tempsPasse) + self.__heureToNb(nouveauLogiciel.getTempsPasse()) )  )) #Permet d'additionner deux heures de formes hh:mm:ss en les convertissant en secodnes puis à nouveau en hh:mm:ss
                            break
                else: #sinon ajouter le nouveau logiciel
                    self.sessionTP.listeLogiciels.append(nouveauLogiciel)        
            else: #sinon ajouter le nouveau logiciel
                self.sessionTP.listeLogiciels.append(nouveauLogiciel)

    def __isEnregistrer(self,texte):
        if "Enregistrer" in texte:
            return True  
        elif "Save" in texte:
            return True  
        else:
            return False
    
    def __isCompiler(self, texte):
        if texte == "Compiler":
            return True  
        elif texte == "Build":
            return True
        elif texte == "Build and run":
            return True
        else:
            return False
        
    def __getSpecificChild(self, element, tag):
        """
        Recupérer une balise enfant ayant un nom spécial
        """
        for child in element.getchildren():
            if child.tag == tag:
               return child
           
    def __heureToNb(self, heure):
        """
        Convertit une string représentant une heure en secondes
        """
        (h, m, s) = heure.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)    
        
    def __getSpecificAttribute(self, element, nomAttribut):
        """
        Recupérer la valeur d'un attribut depuis une balise
        """
        result = "None"
        for attribut in element.items():
            if attribut[0] == nomAttribut: #attribut[0] = nom de l'attribut, attribut[1] = valeur de l'attribut
                result = attribut[1]
        return result
            
    def __supprimerFichierFusionne(self, nomFichier):
        """
        Supprimer le fichier fusionné
        """
        remove(nomFichier)
