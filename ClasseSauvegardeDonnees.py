# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:53:41 2020

@author: Louison VINCENT
"""

from lxml import etree

class SauvegardDonnee:
    """
    Classe qui permet l'écriture d'un fichier consolidé
    Pour l'instant elle ne se préocupe pas que :
        - les valeurs passées aux fonctions sont au bon format (string)
        - les valeurs soient cohérentes (une action d'un logiciel peut se produire 
          en dehors de la période d'utilisation du logiciel)    
    """
    
    def __init__(self):
        """
        Définit la racine du fichier consolidé et les informations concernant les traces
        """
        self.root = etree.Element("fichierConsolidé")
        self.infoTraces = etree.SubElement(self.root, "infoTraces")
        
    def ajoutInfoEtudiant(self,nomUser,numTP,nomExo):
        """
        Permet d'ajouter les informations (identifiant, groupe de TP, exercice réalisé) de l'étudiant au fichier consolidé
        """
        infoEtud = etree.SubElement(self.root, "infoEtudiant")

        identifiant = etree.SubElement(infoEtud, "identifiant")
        identifiant.text = nomUser

        tp = etree.SubElement(infoEtud, "TP")
        tp.text = numTP
        
        exo = etree.SubElement(infoEtud, "Exercice")
        exo.text = nomExo
        
    def ajoutLogiciel(self, nomLogiciel, hDeb, hFin, actions):
        """
        Ajoute un logiciel à l'arborescence XML et ses informations associées :
            son nom
            son heure de début d'utilisation
            son heure de fin d'utilisation
            ses actions associées, contenu dans une liste de dictionnaire
        """
        logiciel = etree.SubElement(self.infoTraces, nomLogiciel)
        tpsDeb = etree.SubElement(logiciel, "HeureDebut")
        tpsDeb.text = hDeb
        tpsFin = etree.SubElement(logiciel, "HeureFin")
        tpsFin.text = hFin
        
        acts = etree.SubElement(logiciel, "Actions")
        for uneAction in actions:
            act = etree.SubElement(acts, uneAction.get("nomAction"))
            act.set("heure", uneAction.get("heure"))
            act.text = uneAction.get("valeur")
            
    def sauvegardeFichier(self, nomFichier):
        """
        Permet la sauvegarde de l'arborescence créée dans un fichier
        """
        etree.ElementTree(self.root).write(nomFichier, pretty_print = True, xml_declaration=True, encoding="utf-8")