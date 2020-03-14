# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 21:57:50 2020

@author: Moi
"""

from ClassGestionPSR import GestionPSR
import time

monPSR = GestionPSR("C:/Users/Moi/Documents/DUT Projet/Code","test9")

monPSR.lancer()

time.sleep(3)

monPSR.arreter()
