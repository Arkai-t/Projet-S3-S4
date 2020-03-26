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
