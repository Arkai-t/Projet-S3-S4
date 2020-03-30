# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:28:03 2020

@author: paul6
"""
from lxml import etree


from ClassLogiciel import *


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
       
def heureToNb(heure):
        (h, m, s) = heure.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)    
    
def getSpecificAttribute(element, nomAttribut): 
    for attribut in element.items():
        if attribut[0] == nomAttribut:
            return attribut[1]
        
       
       
sessionTP = Session()

#ouverture du xml

tree = etree.parse("testFichierFusionné.xml")

#infos de session
session = tree.xpath("/Report/UserActionData/RecordSession")
attrSession = session[0].items() #get all recordsession attributes


sessionTP.heureDebut = attrSession[1][1]
sessionTP.heureFin = attrSession[2][1]

listeEachActions = session[0].getchildren()

for i,action in enumerate(listeEachActions):
    
    attributsActions = action.items()
    
    #get nom et creation du logiciel
    nomLogiciel = attributsActions[6][1]
    heureAction = attributsActions[1][1]
    nouveauLogiciel = Logiciel(nomLogiciel)
    
    #remplir les actions
    
    
    balisesDeEachAction = action.getchildren()
    
    isActionSpeciale = False
    
    baliseAction = getSpecificChild(action,"Action")
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
        balise = getSpecificChild(action,"Action")
        nouvelleAction.setType(balise.text)
        balise = getSpecificChild(action,"Description")        
        nouvelleAction.description = balise.text
        balise = getSpecificChild(action,"UIAStack")
        #Traitement du UIAStack
        nouvelleAction.setNomPageFromUIAStack(balise)
        
        nouvelleAction.heureDebut = heureAction
        nouvelleAction.setNom()
        if i != 0:
            nouveauLogiciel.addAction(nouvelleAction,heureToNb(heureAction)-heureToNb(getSpecificAttribute(action.getprevious(),"Time")))
            print(heureToNb(heureAction)-heureToNb(getSpecificAttribute(action.getprevious(),"Time")))
        nouveauLogiciel.setHeureDebut()
        
    #Si c'est un texte
    if typeAction == "Saisie":
        for baliseTexte in balisesDeEachAction:
            if baliseTexte.tag == "texte":
                #Création et remplissage de l'actionSaisie
                nouvelleAction = ActionSaisie()
                attributsTextes = baliseTexte.items()
                balise = getSpecificChild(action,"Action")
                nouvelleAction.setType(balise.text)
                balise = getSpecificChild(action,"Description")        
                nouvelleAction.description = balise.text
                balise = getSpecificChild(action,"UIAStack")
                #Traitement du UIAStack
                nouvelleAction.setNomPageFromUIAStack(balise)
                
                nouvelleAction.heureDebut = attributsTextes[0][1]  
                nouvelleAction.phrase = baliseTexte.text
                nouvelleAction.setNom()
                if i != 0:
                    nouveauLogiciel.addAction(nouvelleAction,heureToNb(heureAction)-heureToNb(getSpecificAttribute(action.getprevious(),"Time")))
                nouveauLogiciel.setHeureDebut()
                
                
                print("Action saisie cree")
                
                #Determiner si c'est un enregistrement en cherchant "CTRL-S" dans la chaine de caracteres
                if "Ctrl+S" in baliseTexte.text:
                    
                    nouvelleActionEnregistrer = ActionEnregistrer()
                    nouvelleActionEnregistrer.setType("Enregistrement") #Sera set grace à l'héritage à Enregistrement quoi que ce soit
                    nouvelleActionEnregistrer.setDescription("L'utilisateur a enregistré en appuyant sur Ctrl+S")
                    nouvelleActionEnregistrer.heureDebut = attributsTextes[0][1]
                    balise = getSpecificChild(action,"UIAStack")

                    #Traitement du UIAStack
                    nouvelleAction.setNomPageFromUIAStack(balise)
                                            
                    nouvelleActionEnregistrer.setNom()                    
                    nouveauLogiciel.listeActions.append(nouvelleActionEnregistrer)
                    nouveauLogiciel.setHeureDebut()
                
    
 


    #ajout (ou modif du logiciel)
    if (sessionTP.listeLogiciels):
        if(nouveauLogiciel.nom in sessionTP.getNoms()):
            #Ajouter les actions de nouveauLogiciel au logiciel déjà présent dans listeLogiciels
            for logiciel in sessionTP.listeLogiciels:
                if logiciel.nom == nomLogiciel:
                    logiciel.tempsPasse += nouveauLogiciel.getTempsPasse()
                    logiciel.setHeureDebut()
                    logiciel.listeActions += nouveauLogiciel.listeActions
                    break
        else:
            sessionTP.listeLogiciels.append(nouveauLogiciel)        
    else:
        nouvelleAction.setNom()
        sessionTP.listeLogiciels.append(nouveauLogiciel)
        
        

for logiciel in sessionTP.listeLogiciels:
    print("------------------------------------")
    print("Logiciel : ", logiciel.nom, " (", logiciel.heureDebut,")")
    print("Temps passé : ",logiciel.tempsPasse, "seconde(s)")
    for action in logiciel.listeActions:
        print("-  Nom de l'action: ", action.nom, " ")
        print("   Type de l'action: ", action.type, " (", action.heureDebut,")")
        print("   Description: ", action.description)
        print("   Nom de la Page: ", action.nomPage)
        if isinstance(action ,ActionSaisie):
            print("   Phrase: ", action.phrase)     
        print("--")
        
                
