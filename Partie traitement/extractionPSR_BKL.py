# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 11:28:03 2020

@author: paul6
"""
from lxml import etree

from classLogiciels import Logiciel
from classLogiciels import Action
from classLogiciels import Session



sessionTP = Session()

#ouverture du xml

tree = etree.parse("wow.xml")

#infos de session
session = tree.xpath("/Report/UserActionData/RecordSession")
attrSession = session[0].items() #get all recordsession attributes


sessionTP.heureDebut = attrSession[1][1]
sessionTP.heureFin = attrSession[2][1]
sessionTP.actionCount = attrSession[3][1]

listeEachActions = session[0].getchildren()

for action in listeEachActions:
    attributsActions = action.items()
    
    #get nom et creation du logiciel
    nomLogiciel = attributsActions[6][1]
    heureAction = attributsActions[1][1]
    nouveauLogiciel = Logiciel(nomLogiciel)
    
    #remplir les actions
    
    nouvelleAction = Action()
    
    balisesDeEachAction = action.getchildren()
    
    for balise in balisesDeEachAction:
        if balise.tag == "Action":
            nouvelleAction.type = balise.text
        if balise.tag == "Description":
            nouvelleAction.description = balise.text
        if balise.tag == "UIAStack":
            #Traitement du UIAStack
            levels = balise.getchildren()
            for level in levels: #parcours de toutes les balises level   any('Name' in attr[0] for attr in levelAttributs
                levelAttributs = level.items()
                if nouvelleAction.localisationAction == "": #prendre le premier qui a une balise Name
                    for attribut in levelAttributs:
                        if attribut[0] == "Name":
                            nouvelleAction.localisationAction = attribut[1]
                if nouvelleAction.nomPage == "":
                    for i, attribut in enumerate(levelAttributs):
                        if attribut[0] == "LocalizedControlType" and attribut[1] == "fenêtre":
                            nouvelleAction.nomPage = levelAttributs[i-1][1]
        if balise.tag == "texte":
            texteAttributs = balise.items()
            nouvelleAction.addMot(balise.text, texteAttributs[0][1], texteAttributs[1][1])
            
        
    nouvelleAction.heureDebut = heureAction
    
    
    nouveauLogiciel.listeActions.append(nouvelleAction)
    nouveauLogiciel.setHeureDebut()
    
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
        print("   Localisation: ", action.localisationAction)
        print("   Nom de la Page: ", action.nomPage)
        print("   Mots: ")
        for mot in action.mots:
            print("     ", mot[0], " (", mot[1], " - ", mot[2], ")")
