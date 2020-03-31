# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:29:56 2020

@author: paul6
"""

from ClassPreparationFichiers import PreparationFichiers
from ClassAjoutBKLaPSR import FichierFusionne
from ClassCreationFichierConsolide import FichierConsolide

gest = PreparationFichiers()
gest.preparerFichiers()

bkl = FichierFusionne()
bkl.ajoutDuBKLaPSR()

monFicConsolide = FichierConsolide()
monFicConsolide.recupererInformations()
monFicConsolide.creerArborescence()
monFicConsolide.sauvegardeFichier()
