# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:42:44 2020
@author: Louison
"""

#tester avec le supprimerLogBKL

from os import path, remove, listdir, rename
from zipfile import ZipFile
from shutil import move,rmtree #Cette bibliothèque est basée sur celle d'os
from json import load

"""
Chemins des paramètres du projet
"""
pathConfig = r".\Config_traitement.json"

#Récupérer la configuration du traitement
file = open(pathConfig, encoding='utf-8')
data = load(file)
file.close()
repertoirePartieEtudiant = data["parametres"]["repertoirePartieEtudiant"]
print(repertoirePartieEtudiant)
repertoireStockageFichiers = data["repertoireStockageFichiers"]
nomFic = data["parametres"]["nomFic"]

"""
Nom du fichier BKL
"""
nomFicBKL = "kpc_log.tsv"

class PreparationFichiers:
     """
     Cette classe sert à préparer les fichiers générés par l'interface élève, et à les déplacer
     dans le repertoireStockageFichiers
     """
     def __init__(self):
        #Le nom du fichier de PSR pourra peut être être lue depuis un fichier de configuration/information
        self.nomFic = nomFic
        self.pathToPSR = repertoirePartieEtudiant
        self.pathToBKL = repertoirePartieEtudiant + r"\basicKeyLogger\data"

     @property
     def nomZipPSR(self):
          #Ouvrir le fichier Config_etudiant.json pour récupérer le nom du Fichier temporaire de PSR
          fileEtud = open(data["parametres"]["repertoirePartieEtudiant"] + r"\Config_etudiant.json")
          dataEtud = load(fileEtud)
          fileEtud.close()
          return dataEtud["nomFicTempPSR"]

     def fichierTracesCreer(self):
        """
        Vérifie la présence des fichiers utiles aux traitements des traces :
            - nomFicBKL
            - .xml dans le zip généré par PSR
        """
        assert self.nomFic != ""
        return ((path.exists(self.pathToBKL + '\\' + nomFicBKL)) and (path.exists(self.pathToPSR + '\\' + self.nomZipPSR)))

     def __deziperPSR(self):
         #Dézipage du fichier de PSR
         with ZipFile(self.pathToPSR + "\\" + self.nomZipPSR, 'r') as zip_ref:
               zip_ref.extractall(self.pathToPSR + "\\" + self.nomFic) #Prend en paramètre le dossier où va les fichiers

         #Suppression du .zip
         remove(self.pathToPSR + "\\" + self.nomZipPSR)

     def __renommerFicPSR(self):
        """
        Renomme l'unique fichier XML généré
        """
        listeDocs = listdir(self.pathToPSR + "\\" + self.nomFic)

        for fichier in listeDocs:
             if fichier.endswith(".xml"):
                 rename((self.pathToPSR + "\\" + self.nomFic + "\\" + fichier), (self.pathToPSR + "\\" + self.nomFic + "\\" + self.nomFic + ".xml"))
                 #Génére une erreur si abscence de break => essaye de renommer le fichier qui vient d'être renommé
                 break

     def __deplacerFicPSR(self):
        """
        Déplace le fichier XML dans le repertoire de stockage des traces
        """
        move(self.pathToPSR + '\\' + self.nomFic + '\\' + self.nomFic + '.xml', repertoireStockageFichiers)

     def __supprimerRepertoirePSR(self):
        """
        Supprime le répertoire de PSR dézippé
        """
        rmtree((self.pathToPSR + '\\' + self.nomFic), True)

     def __preparerFicPSR(self):
        """
        Prépare les fichiers de PSR pour leurs traitements ultérieurs
        """
        self.__deziperPSR()

        self.__renommerFicPSR()

        self.__deplacerFicPSR()

        self.__supprimerRepertoirePSR()

     def __deplacerFicBKL(self):
        """
        Déplace le fichier kpc_log.tsv dans le repertoire de stockage des traces
        """
        move(self.pathToBKL + "\\" + nomFicBKL, repertoireStockageFichiers)

     def __clearRepertoireDataBKL(self):
        """
        Retire tous les fichiers du repertoire data de Basic Key Logger
        """
        for fichier in listdir(self.pathToBKL):
            remove(self.pathToBKL + '\\' + fichier)

     def __renommerFicBKL(self):
          """
          Renomme le fichier key_log.tsv contenu dans Stockage fichiers
          """
          rename((repertoireStockageFichiers + '\\' + nomFicBKL), (repertoireStockageFichiers + '\\' + self.nomFic + '.tsv'))

     def __preparerFicBKL(self):
        """
        Prépare les fichiers de Basic Key Logger pour leurs traitements ultérieurs
        """
        self.__deplacerFicBKL()

        self.__clearRepertoireDataBKL()

        self.__renommerFicBKL()

     def preparerFichiers(self):
        if (self.fichierTracesCreer()):
            self.__preparerFicPSR()
            self.__preparerFicBKL()
        else:
            print("Un des fichiers est manquant, ou à mal été nommmé")
