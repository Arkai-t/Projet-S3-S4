# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:29:56 2020

@author: paul6
"""

from ClassPreparationFichiers import PreparationFichiers
from ClassAjoutBKLaPSR import FichierFusionne
from ClassCreationFichierConsolide import FichierConsolide

print('Preparation des fichiers en cours')
gest = PreparationFichiers()
gest.preparerFichiers()
print('Preparation des fichiers effectuée')


print('Creation du fichier fusionne en cours')
bkl = FichierFusionne()
bkl.ajoutDuBKLaPSR()
print('Creation du fichier fusionne terminée')


print('Creation du fichier consolidé en cours')
monFicConsolide = FichierConsolide()
monFicConsolide.recupererInformations()
monFicConsolide.creerArborescence()
monFicConsolide.sauvegardeFichier()
print('Creation du fichier consolidé terminée')
