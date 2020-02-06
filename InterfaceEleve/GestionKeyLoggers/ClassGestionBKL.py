# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 19:08:37 2020
@author: Louison VINCENT
"""

import os

#Location de BKL
pathBKL = r"C:/Users/Moi/Documents/DUT Projet/basicKeyLogger/"

class GestionBKL:
    def __init__(self):
        pass

    def lancer(self):
        """
        Lance le logiciel BKL
        """
        os.system("startHidden.exe")



    def arreter(self):
        """
        Arrête BKL
        """
        os.system("stopKeyLogger.exe")

