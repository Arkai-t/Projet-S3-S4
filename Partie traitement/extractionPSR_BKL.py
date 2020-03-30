# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:28:03 2020

@author: paul6
"""
from lxml import etree


from classLogiciels import *


def isEnregistrer(texte):
    if texte == "Enregistrer":
        return True  
    elif texte == "Save":
        return True  
    elif texte == "Enregistrer Sous":
        return True
    else:
        return False

def isCompiler(texte):
    if texte == "Compiler":
        return True  
    elif texte == "Build":
        return True
    else:
        return False
    
def getSpecificChild(element, tag):
   for child in element.getchildren():
       if child.tag == tag:
           return child
       
       
sessionTP = Session()

#ouverture du xml

tree = etree.parse("wow.xml")

#infos de session
session = tree.xpath("/Report/UserActionData/RecordSession")
attrSession = session[0].items() #get all recordsession attributes


sessionTP.heureDebut = attrSession[1][1]
sessionTP.heureFin = attrSession[2][1]

listeEachActions = session[0].getchildren()

for action in listeEachActions:
    attributsActions = action.items()
    
    #get nom et creation du logiciel
    nomLogiciel = attributsActions[6][1]
    heureAction = attributsActions[1][1]
    nouveauLogiciel = Logiciel(nomLogiciel)
    
    #remplir les actions
    
    
    balisesDeEachAction = action.getchildren()
    
    isActionSpeciale = False
    
    
    for baliseAction in balisesDeEachAction:
        if baliseAction.tag == "Action":
            typeAction = baliseAction.text.split(" ",1)[0]
            if typeAction == "Clic": #Savoir si c'est clic
                #Savoir de quel type d'action de clic est l'action
                UIAStack = getSpecificChild(action, "UIAStack")
                for level in UIAStack.getchildren(): #Chaque balise level
                    for attribut in level.items():  #chaque attributs de la balise level
                        if attribut[0] == "Name":
                            if isEnregistrer(attribut[1]):
                                nouvelleAction = ActionEnregistrer()
                                isActionSpeciale = True
                                break
                            if isCompiler(attribut[1]):
                                nouvelleAction = ActionCompiler()
                                isActionSpeciale = True
                                break
                    
                
                    
                if isActionSpeciale == False:
                    nouvelleAction = ActionClic()          
                    
                #Remplir
                for balise in balisesDeEachAction:
                    if balise.tag == "Action":
                        nouvelleAction.setType(balise.text)
                    if balise.tag == "Description":
                        nouvelleAction.description = balise.text
                    if balise.tag == "UIAStack":
                        #Traitement du UIAStack
                        levels = balise.getchildren()
                        for level in levels: #parcours de toutes les balises level   any('Name' in attr[0] for attr in levelAttributs
                            levelAttributs = level.items()
                            if nouvelleAction.nomPage == "":
                                for i, attribut in enumerate(levelAttributs):
                                    if attribut[0] == "LocalizedControlType" and attribut[1] == "fenêtre":
                                        nouvelleAction.nomPage = levelAttributs[i-1][1]
                
                nouvelleAction.heureDebut = heureAction
                
                nouveauLogiciel.listeActions.append(nouvelleAction)
                nouveauLogiciel.setHeureDebut()
                
            #Si c'est un texte
            if typeAction == "Saisie":
                for baliseTexte in balisesDeEachAction:
                    if baliseTexte.tag == "texte":
                        #Création et remplissage de l'actionSaisie
                        nouvelleAction = ActionSaisie()
                        
                        attributsTextes = baliseTexte.items()
                        for balise in balisesDeEachAction:
                            if balise.tag == "Action":
                                nouvelleAction.setType(balise.text)
                            if balise.tag == "Description":
                                nouvelleAction.description = balise.text
                                     
                            if balise.tag == "UIAStack":
                                #Traitement du UIAStack
                                levels = balise.getchildren()
                                for level in levels: #parcours de toutes les balises level   any('Name' in attr[0] for attr in levelAttributs
                                    levelAttributs = level.items()
                                    if nouvelleAction.nomPage == "":
                                        for i, attribut in enumerate(levelAttributs):
                                            if attribut[0] == "LocalizedControlType" and attribut[1] == "fenêtre":
                                                nouvelleAction.nomPage = levelAttributs[i-1][1]
                        
                        nouvelleAction.heureDebut = attributsTextes[0][1]  
                        nouvelleAction.phrase = baliseTexte.text
                        
                        nouveauLogiciel.listeActions.append(nouvelleAction)
                        nouveauLogiciel.setHeureDebut()
                        
                        
                        print("Action saisie cree")
                        
                        #Determiner si c'est un enregistrement en cherchant "CTRL-S" dans la chaine de caracteres
                        if "Ctrl+S" in baliseTexte.text:
                            
                            nouvelleActionEnregistrer = ActionEnregistrer()
                            nouvelleActionEnregistrer.setType("Enregistrement") #Sera set grace à l'héritage à Enregistrement quoi que ce soit
                            nouvelleActionEnregistrer.setDescription("L'utilisateur a enregistré en appuyant sur Ctrl+S")
                            nouvelleActionEnregistrer.heureDebut = attributsTextes[0][1]
                            for balise in balisesDeEachAction:   
                                if balise.tag == "UIAStack":
                                    #Traitement du UIAStack
                                    levels = balise.getchildren()
                                    for level in levels: #parcours de toutes les balises level   any('Name' in attr[0] for attr in levelAttributs
                                        levelAttributs = level.items()
                                        if nouvelleActionEnregistrer.nomPage == "":
                                            for i, attribut in enumerate(levelAttributs):
                                                if attribut[0] == "LocalizedControlType" and attribut[1] == "fenêtre":
                                                    nouvelleActionEnregistrer.nomPage = levelAttributs[i-1][1]
                        
                            nouveauLogiciel.listeActions.append(nouvelleActionEnregistrer)
                            nouveauLogiciel.setHeureDebut()
                        
            
            break


    #ajout (ou modif du logiciel)
    if (sessionTP.listeLogiciels):
        if(nouveauLogiciel.nom in sessionTP.getNoms()):
            #Ajouter les actions de nouveauLogiciel au logiciel déjà présent dans listeLogiciels
            for logiciel in sessionTP.listeLogiciels:
                if logiciel.nom == nomLogiciel:
                    logiciel.setHeureDebut()
                    logiciel.listeActions += nouveauLogiciel.listeActions
                    break
        else:
            sessionTP.listeLogiciels.append(nouveauLogiciel)        
    else:
        sessionTP.listeLogiciels.append(nouveauLogiciel)
        
        

for logiciel in sessionTP.listeLogiciels:
    print("------------------------------------")
    print("Logiciel : ", logiciel.nom, " (", logiciel.heureDebut,")")
    for action in logiciel.listeActions:
        print("- Nom de l'action: ", action.type, " (", action.heureDebut,")")
        print("   Description: ", action.description)
        print("   Nom de la Page: ", action.nomPage)
        if isinstance(action ,ActionSaisie):
            print("   Phrase: ", action.phrase)     
        print("--")
                
