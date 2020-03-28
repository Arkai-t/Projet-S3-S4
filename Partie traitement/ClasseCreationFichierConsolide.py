# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:53:41 2020

@author: Louison VINCENT
"""

from lxml import etree
from ClassSession import Session
from json import load

"""
Chemins des paramètres du projet
"""
pathConfig = r"D:\Documents\Python Scripts\Config.json"

class SauvegardDonnee:
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

    def creerArborescence(self, maSession):
        heureDebut = etree.SubElement(self.root, "HeureDebut")
        heureDebut.text = maSession.getHeureDebut()

        heureFin = etree.SubElement(self.root, "HeureFin")
        heureFin.text = maSession.getHeureFin()

        logiciels = etree.SubElement(self.root, "Logiciels")

        for logicielCourant in maSession.getLogiciels():
             #Créer un logiciel
             logiciel = etree.SubElement(logiciels, logicielCourant.getNom())

             heureDebutLogiciel = etree.SubElement(logiciel, "HeureDebut")
             heureDebutLogiciel.text = logicielCourant.getHeureDebut()

             heureFinLogiciel = etree.SubElement(logiciel, "HeureFin")
             heureFinLogiciel.text = logicielCourant.getHeureFin()

             actions = etree.SubElement(logiciel, "Actions")

             for actionCourante in logicielCourant.getActions():
                  action = etree.SubElement(actions, actionCourante.getType()) #Nom de l'action peut être fait autrement

                  heureDebut = etree.SubElement(action, "HeureDebut")
                  heureDebut.text = actionCourante.getHeureDebut()


    def sauvegardeFichier(self, nomFichier = ""):
        """
        Permet la sauvegarde de l'arborescence créée dans un fichier
        """
        #Récupérer la configuration
        file = open(pathConfig)
        data = load(file)
        file.close()
        etree.ElementTree(self.root).write((data["nomFic"] + "_FichierConsolide.xml"), pretty_print = True, xml_declaration=True, encoding="utf-8")
