# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:42:44 2020
@author: Moi
"""

#tester avec le supprimerLogBKL

import os
import zipfile
import shutil #Cette bibliothèque est basée sur celle d'os
from json import load

"""
Chemins des paramètres du projet
"""
pathConfig = r"D:\Documents\Python Scripts\Config.json"

#Récupérer la configuration
file = open(pathConfig)
data = load(file)
file.close()
repertoirePartieEtudiant = data["repertoirePartieEtudiant"]
repertoireStockageFichiers = data["repertoireStockageFichiers"]

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
        self.nomZipPSR = data["PSR"]["nomFicTempPSR"]
        self.nomFic = data["nomFic"]
        self.pathToPSR = repertoirePartieEtudiant
        self.pathToBKL = repertoirePartieEtudiant + r"\basicKeyLogger\data"

     def fichierTracesCreer(self):
        """
        Vérifie la présence des fichiers utiles aux traitements des traces :
            - nomFicBKL
            - .xml dans le zip généré par PSR
        """
        return ((os.path.exists(self.pathToBKL + '\\' + nomFicBKL)) and (os.path.exists(self.pathToPSR + '\\' + self.nomZipPSR)))

     def __deziperPSR(self):
         #Dézipage du fichier de PSR
         with zipfile.ZipFile(self.pathToPSR + "\\" + self.nomZipPSR, 'r') as zip_ref:
               zip_ref.extractall(self.pathToPSR + "\\" + self.nomFic) #Prend en paramètre le dossier où va les fichiers

         #Suppression du .zip
         os.remove(self.pathToPSR + "\\" + self.nomZipPSR)

     def __renommerFicPSR(self):
        """
        Renomme l'unique fichier XML généré
        """
        listeDocs = os.listdir(self.pathToPSR + "\\" + self.nomFic)

        for fichier in listeDocs:
             if fichier.endswith(".xml"):
                 os.rename((self.pathToPSR + "\\" + self.nomFic + "\\" + fichier), (self.pathToPSR + "\\" + self.nomFic + "\\" + self.nomFic + ".xml"))
                 #Génére une erreur si abscence de break => essaye de renommer le fichier qui vient d'être renommé
                 break

     def __deplacerFicPSR(self):
        """
        Déplace le fichier XML dans le repertoire de stockage des traces
        """
        shutil.move(self.pathToPSR + '\\' + self.nomFic + '\\' + self.nomFic + '.xml', repertoireStockageFichiers)

     def __supprimerRepertoirePSR(self):
        """
        Supprime le répertoire de PSR dézippé
        """
        shutil.rmtree((self.pathToPSR + '\\' + self.nomFic), True)

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
        shutil.move(self.pathToBKL + "\\" + nomFicBKL, repertoireStockageFichiers)

     def __clearRepertoireDataBKL(self):
        """
        Retire tous les fichiers du repertoire data de Basic Key Logger
        """
        for fichier in os.listdir(self.pathToBKL):
            os.remove(self.pathToBKL + '\\' + fichier)

     def __renommerFicBKL(self):
          """
          Renomme le fichier key_log.tsv contenu dans Stockage fichiers
          """
          os.rename((repertoireStockageFichiers + '\\' + nomFicBKL), (repertoireStockageFichiers + '\\' + self.nomFic + '.tsv'))

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
