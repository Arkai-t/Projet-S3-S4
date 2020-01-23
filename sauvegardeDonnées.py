# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 10:58:27 2019

@author: Louison VINCENT
"""

#Importation de la classe
from ClasseSauvegardeDonnees import SauvegardDonnee

#Création de la classe
monXML = SauvegardDonnee()
#Ajout des informations de l'étudiant
monXML.ajoutInfoEtudiant("identifiantUser", "TPX", "Exo X")

#Création de la liste qui contient les actions
actionsLogi1 = []
#Création d'une action
action1 = {}
action1["nomAction"] = "Ecrire"
action1["heure"] = "14:20:18"
action1["valeur"] = "CTRL+C"
actionsLogi1.append(action1)

#Ajout du logiciel et des informations correspondantes
monXML.ajoutLogiciel("logiciel1", "14:18:03", "16:02:54", actionsLogi1)

#Création de la liste qui contient les actions
actionsLogi2 = []
#Création d'une action
action1 = {}
action1["nomAction"] = "Menu"
action1["heure"] = "14:48:56"
action1["valeur"] = "Compiler"
actionsLogi2.append(action1)

#Création d'une action
action2 = {}
action2["nomAction"] = "Menu"
action2["heure"] = "15:38:33"
action2["valeur"] = "Sauvegarder"
actionsLogi2.append(action2)
#Ajout du logiciel et des informations correspondantes
monXML.ajoutLogiciel("logiciel2", "14:36:36", "15:48:58", actionsLogi2)

#Écriture du fichier XML
monXML.sauvegardeFichier("exempleDeTest_FichierConsolide.xml")