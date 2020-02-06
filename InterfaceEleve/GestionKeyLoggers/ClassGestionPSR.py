# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:51:51 2020
@author: Louison VINCENT
"""

import subprocess
import zipfile
import os
from os import path

#Location de PSR
pathPSR = "C:/Windows/System32/psr.exe"

class GestionPSR:
    def __init__(self, cheminEnregistrement, nomFichier):
        """
        Définit le chemin où les fichiers produits vont être enregistrées et le nom du fichier enregistré
        """
        self.cheminEnregistrement = cheminEnregistrement
        self.nomFichier = nomFichier

    @property
    def sortieZip(self):
        return r'{0}/{1}.zip'.format(self.cheminEnregistrement, self.nomFichier)

    @property
    def sortieFichier(self):
        return r"{0}/{1}/".format(self.cheminEnregistrement, self.nomFichier)

    def lancer(self):
        """
        Lance le logiciel PSR avec comme paramètres:
            /start : lancer PSR
            /arcxml 1 : produire un fichier de traces XML
            /sc 0 : ne pas faire de capture d'écran
            /gui 0 : cacher l'interface de PSR
            /output dossier de sortie des fichiers
        """
        assert(len(self.nomFichier) <= 5)

        subprocess.Popen([pathPSR , "/start" , "/arcxml", "1" , "/sc", "0", "/gui", "0" , "/output" , self.sortieZip], shell=True)

    def __deziper(self):
         #Dézipage
         with zipfile.ZipFile(self.sortieZip, 'r') as zip_ref:
               zip_ref.extractall(r"{0}/{1}".format(self.cheminEnregistrement, self.nomFichier))

         #Suppression du .zip
         os.remove(self.sortieZip)

    def __supprimer(self):
         """
         Supprimer tous les fichier .mht du dossier extrait du zip
         """
         listeDocs = os.listdir(self.sortieFichier)

        #Parcours des fichiers pour supprimer tous les .MHT
         for fichier in listeDocs:
             if fichier.endswith(".mht"):
                 os.remove(os.path.join(self.sortieFichier, fichier))

    def __renommer(self):
        """
        Renomme l'unique fichier XML généré
        """
        listeDocs = os.listdir(self.sortieFichier)

        for fichier in listeDocs:
             if fichier.endswith(".xml"):
                 os.rename((self.sortieFichier + fichier), (self.sortieFichier + self.nomFichier + ".xml"))
             #Génére une erreur si abscence de break => essaye de renommer le fichier qui vient d'être renommé
             break

    def arreter(self):
        """
        Arrête PSR, et prépare les fichiers produits pour la fusion avec BKL
        """
        subprocess.Popen([pathPSR , "/stop"],  shell=True)

        #Attendre que PSR créé le zip
        while path.isfile(self.sortieZip) != True:
            pass

        self.__deziper()

        self.__supprimer()

        self.__renommer()
