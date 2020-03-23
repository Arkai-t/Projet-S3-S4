# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 19:08:37 2020
@author: Louison VINCENT
"""

from subprocess import Popen
from os import chdir
from json import load

pathConfig = r"D:\Documents\Python Scripts\Config.json"

#Récupérer la configuration
file = open(pathConfig)
data = load(file)
file.close()
pathBKL = data["repertoirePartieEtudiant"]


class GestionBKL:
    def __init__(self):
        chdir(pathBKL + r"\basicKeyLogger") #Positionner le répertoire de travaille sur celui de Basic KeyLogger

    def lancer(self):
        """
        Lance le logiciel BKL
        """
        Popen(["startHidden.exe"], shell=True)




    def arreter(self):
        """
        Arrête BKL
        """
        Popen(["stopKeyLogger.exe"], shell=True)
