# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 19:22:34 2020

@author: Moi
"""

from ClassGestionBKL import GestionBKL
import time

monBKL = GestionBKL()

monBKL.lancer()

time.sleep(3)

monBKL.arreter()