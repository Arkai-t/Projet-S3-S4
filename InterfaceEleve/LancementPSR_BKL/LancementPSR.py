# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:43:39 2020

@author: Paul Lafourcade
"""

#C'est un fichier de test

import time
import subprocess
import zipfile
import os

subprocess.Popen(["psr" , "/start" , "/arcxml", "1" , "/sc", "0", "/gui", "0" , "/output" , r"traces\testPsr1.zip"], shell=True)

time.sleep(10)

subprocess.Popen(["psr" , "/stop"],  shell=True)

time.sleep(3) #attendre que le fichier se crée avant de dézip

#--------DEZIP--------------------------

with zipfile.ZipFile(r"traces\testPsr1.zip", 'r') as zip_ref:
    zip_ref.extractall(r"traces\unzip") #CHOISIR UN NOM DE DOSSIER
    
#-------DELETE HTM--------------------------

dossier = "./traces/unzip/"
listeDocs = os.listdir(dossier)

for fichier in listeDocs:
    if fichier.endswith(".mht"):
        os.remove(os.path.join(dossier, fichier))
        print(fichier," supprimé avec succès")
        
#A faire:
#Renommer fichier XML, Choisir nom des dossiers / fichiers
