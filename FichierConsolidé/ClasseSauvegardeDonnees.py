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
        - de l'effacement de valeurs'
    """

    def __init__(self,nomUser,numTP,nomExo):
        """
        Définit la racine du fichier consolidé et les informations concernant les traces
        Prend en paramètre:
             - le nom/identifiant de l'étudiant ayant fait l'exercice
             - son numéro de TP
             - le nom/identifiant de l'exercice réalisé'
        """
        #Création de la racine
        self.root = etree.Element("fichierConsolidé")

        #Creation du noeud infoTraces qui contiendra toutes les informations des traces
        self.infoTraces = etree.SubElement(self.root, "infoTraces")
        #Creation du noeud infoEtudiant qui contiendra toutes les informations de l'étudiant
        self.infoEtud = etree.SubElement(self.root, "infoEtudiant")

        identifiant = etree.SubElement(self.infoEtud, "identifiant")
        identifiant.text = nomUser

        tp = etree.SubElement(self.infoEtud, "TP")
        tp.text = numTP

        exo = etree.SubElement(self.infoEtud, "Exercice")
        exo.text = nomExo

    def ajoutLogiciel(self, nomLogiciel, hDeb, hFin, actions):
        """
        Ajoute un logiciel à l'arborescence XML et ses informations associées:
            - son nom
            - son heure de début d'utilisation
            - son heure de fin d'utilisation
            - ses actions associées, contenu dans une liste de dictionnaire
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

    def sauvegardeFichier(self, nomFichier = ""):
        """
        Permet la sauvegarde de l'arborescence créée dans un fichier
        Si aucun nom de fichier n'est donné, le nom par défaut est:
             identifiantEtudiant_FichierConsolide.xml
        """
        #Nom par défaut si il n'est pas définit
        if nomFichier == "":
             nomFichier = self.infoEtud[0].text + "_FichierConsolide.xml"
        etree.ElementTree(self.root).write(nomFichier, pretty_print = True, xml_declaration=True, encoding="utf-8")
