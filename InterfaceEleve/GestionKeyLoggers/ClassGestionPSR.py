# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:51:51 2020
@author: Louison VINCENT
"""

import subprocess
import zipfile
import os
from os import path

class GestionPSR:
    def __init__(self, cheminEnregistrement, nomFichier):
        """
        Définit le chemin où les fichiers produits vont être enregistrées et le nom du fichier enregistré
        """
        self.cheminEnregistrement = cheminEnregistrement
        self.nomFichier = nomFichier

    @property
    def sortieFichier(self):
        return r'{0}/{1}.zip'.format(self.cheminEnregistrement, self.nomFichier)

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

        subprocess.Popen(["C:/Windows/System32/psr.exe" , "/start" , "/arcxml", "1" , "/sc", "0", "/gui", "0" , "/output" , self.sortieFichier], shell=True)

    def __deziper(self):
         #Dézipage
         with zipfile.ZipFile(self.sortieFichier, 'r') as zip_ref:
               zip_ref.extractall(r"{0}/unzip".format(self.cheminEnregistrement)) #CHOISIR UN NOM DE DOSSIER

         #Suppression du .zip
         os.remove(self.sortieFichier)

    def __supprimer(self):
         """
         Supprimer tous les fichier .mht du dossier extrait du zip
         """
         #Supprimer .HTM
         dossier = '{0}/unzip'.format(self.cheminEnregistrement) #CHOISIR LE MEME NOM DE DOSSIER QU'AU DESSUS
         listeDocs = os.listdir(dossier)

        #Parcours des fichiers pour supprimer tous les .MHT
         for fichier in listeDocs:
             if fichier.endswith(".mht"):
                 os.remove(os.path.join(dossier, fichier))

    def arreter(self):
        """
        Arrête PSR, et prépare les fichiers produits pour la fusion avec BKL
        """
        subprocess.Popen(["C:/Windows/System32/psr.exe" , "/stop"],  shell=True)

        #Attendre que PSR créé le fichier
        while path.isfile(self.sortieFichier) != True:
            pass

        self.__deziper()

        self.__supprimer()
