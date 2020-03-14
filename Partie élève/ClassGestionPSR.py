# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:51:51 2020
@author: Louison VINCENT
"""

import subprocess

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

    def arreter(self):
        """
        Arrête PSR, et prépare les fichiers produits pour la fusion avec BKL
        """
        subprocess.Popen([pathPSR , "/stop"],  shell=True)
