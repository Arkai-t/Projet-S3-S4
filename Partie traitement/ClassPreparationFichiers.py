# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:42:44 2020
@author: Moi
"""

import os
import zipfile
import shutil #Cette bibliothèque est basée sur celle d'os

"""
Chemins paramètrables du projet
    - repertoireParteEleve designe le dossier où est stocker l'interface de l'étudiant
    - repertoireStockageFichiers designe l'endroit où sont stocker les traces brutes de l'étudiant
"""
repertoirePartieEtudiant = r"C:\Users\Moi\Documents\DUT\DUT Projet\Code\Partie Élève"
repertoireStockageFichiers = r"C:\Users\Moi\Documents\DUT\DUT Projet\Code\Stockage Traces"

"""
Nom du fichier BKL
"""
nomFicBKL = "kpc_log.tsv"

class PreparationFichiers:
     """
     Cette classe sert à préparer les fichiers générés par l'interface élève, et à les déplacer
     dans le repertoireStockageFichiers
     """
     def __init__(self, nomFicPSR):
        #Le nom du fichier de PSR pourra peut être être lue depuis un fichier de configuration/information
        self.nomZipPSR = nomFicPSR + ".zip"
        self.nomFicPSR = nomFicPSR
        self.pathToPSR = repertoirePartieEtudiant #+ r"\{0}".format(self.nomFicPSR)
        self.pathToBKL = repertoirePartieEtudiant + r"\basicKeyLogger\data"

     def fichierTracesCreer(self):
        """
        Vérifie la présence des fichiers utiles aux traitements des traces :
            - nomFicBKL
            - .xml dans le zip généré par PSR
        """
        return ((os.path.exists(self.pathToBKL + r"\{0}".format(nomFicBKL))) and (os.path.exists(self.pathToPSR)))

     def __deziperPSR(self):
         #Dézipage du fichier de PSR
         with zipfile.ZipFile(self.pathToPSR + "\\" + self.nomZipPSR, 'r') as zip_ref:
               zip_ref.extractall(self.pathToPSR + "\\" + self.nomFicPSR) #Prend en paramètre le dossier où va les fichiers

         #Suppression du .zip
         os.remove(self.pathToPSR + "\\" + self.nomZipPSR)

     def __renommerFicPSR(self):
        """
        Renomme l'unique fichier XML généré
        """
        listeDocs = os.listdir(self.pathToPSR + "\\" + self.nomFicPSR)

        for fichier in listeDocs:
             if fichier.endswith(".xml"):
                 os.rename((self.pathToPSR + "\\" + self.nomFicPSR + "\\" + fichier), (self.pathToPSR + "\\" + self.nomFicPSR + "\\" + self.nomFicPSR + ".xml"))
                 #Génére une erreur si abscence de break => essaye de renommer le fichier qui vient d'être renommé
                 break

     def __deplacerFicPSR(self):
        """
        Déplace le fichier XML dans le repertoire de stockage des traces
        """
        shutil.move(self.pathToPSR + '\\' + self.nomFicPSR + '\\' + self.nomFicPSR + '.xml', repertoireStockageFichiers)

     def __supprimerRepertoirePSR(self):
        """
        Supprime le répertoire de PSR dézippé
        """
        shutil.rmtree(self.pathToPSR + '\\' + self.nomFicPSR)

     def __preparerFicPSR(self):
        """
        Prépare les fichiers de PSR pour leurs traitements ultérieurs
        """
        self.__deziperPSR()

        self.__renommerFicPSR()

        self.__deplacerFicPSR()

        self.__supprimerRepertoirePSR

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

     def __preparerFicBKL(self):
        """
        Prépare les fichiers de Basic Key Logger pour leurs traitements ultérieurs
        """
        self.__deplacerFicBKL()

        self.__clearRepertoireDataBKL()

     def preparerFichiers(self):
        if (self.fichierTracesCreer()):
            self.__preparerFicPSR()
            self.__preparerFicBKL()
        else:
            print("Un des fichiers est manquant, ou à mal été nommmé")
