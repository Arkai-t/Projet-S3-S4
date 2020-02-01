# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:51:51 2020
@author: Louison VINCENT
"""

import time
import subprocess
import zipfile
import os
from shutil import rmtree

class GestionPSR:
    def __init__(self, cheminEnregistrement, nomFichier):
        """
        Définit le chemin où les fichiers produits vont être enregistrées et le nom du fichier enregistré
        """
        self.cheminEnregistrement = cheminEnregistrement
        self.nomFichier = nomFichier
        self.estLance = False

    @property
    def sortieFichier(self):
        return r'{0}\{1}.zip'.format(self.cheminEnregistrement, self.nomFichier)

    def lancer(self):
        """
        Lance le logiciel PSR avec comme paramètres:
            /start : lancer PSR
            /arcxml 1 : produire un fichier de traces XML
            /sc 0 : ne pas faire de capture d'écran
            /gui 0 : cacher l'interface de PSR
            /output dossier de sortie des fichiers
        """
        if (self.estLance == False):
             assert(len(self.nomFichier) < 5)

             self.estLance = True

             #C:\Windows\System32\psr.exe
             subprocess.Popen(["psr" , "/start" , "/arcxml", "1" , "/sc", "0", "/gui", "0" , "/output" , self.sortieFichier], shell=True)

        else:
             print("Le logiciel PSR est déjà lancé !")

    def __deziper(self):
         #Attendre que le fichier se créer avant de le déziper
         time.sleep(3)

          #Dézipage
         with zipfile.ZipFile(self.sortieFichier, 'r') as zip_ref:
               zip_ref.extractall(r"{0}\unzip".format(self.cheminEnregistrement)) #CHOISIR UN NOM DE DOSSIER

         #Supprimer le .zip
         rmtree(self.nomFichier, ignore_errors = True)

    def __supprimer(self):
         """
         Supprimer tous les fichier .mht du dossier extrait du zip
         """
         #Supprimer .HTM
         dossier = '{0}\\unzip'.format(self.cheminEnregistrement) #CHOISIR LE MEME NOM DE DOSSIER QU'AU DESSUS
         listeDocs = os.listdir(dossier)

        #Parcours des fichiers pour supprimer tous les .MHT
         for fichier in listeDocs:
             if fichier.endswith(".mht"):
                 os.remove(os.path.join(dossier, fichier))
                 print(fichier," supprimé avec succès")

    def arreter(self):
        """
        Arrête PSR, et prépare les fichiers produits pour la fusion avec BKL
        """
        if (self.estLance == True):
             #C:\Windows\System32\psr.exe
             subprocess.Popen(["psr" , "/stop"],  shell=True)

             self.__deziper()

             self.__supprimer()

        else:
            print("Le logiciel PSR n'est pas lancé !")
