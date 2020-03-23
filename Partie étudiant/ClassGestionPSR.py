# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 18:51:51 2020
@author: Louison VINCENT
"""

from subprocess import Popen
from json import load, dumps
from os.path import exists

pathConfig = r"D:\Documents\Python Scripts\Config.json"

#Récupérer la configuration
file = open(pathConfig)
data = load(file)
file.close()
pathPSR = data["PSR"]["pathPSR"]

def genererNomFicTemp(pathSauvegarde):
     """
     Génère un nom de fichier n'existant pas dans le pathSauvegarde
     """
     nomFicTemp = "AAAA"
     pathComplet = (pathSauvegarde + '\\' + nomFicTemp + '.zip')
     while (True):
          while (True):
               while (True):
                    while (True):
                         print(nomFicTemp + ' : ' + str(exists(pathComplet)))
                         if not (exists(pathComplet)):
                             break
                         #Incrémenter le caractère courant
                         nomFicTemp =  nomFicTemp[:3] + chr(ord(nomFicTemp[3])+1)
                         #Passer les caractères ASCCI que nous ne voulons pas
                         if (91 <= ord(nomFicTemp[3]) and ord(nomFicTemp[3]) <= 96):
                              nomFicTemp = nomFicTemp[:3] + 'a'
                         pathComplet = (pathSauvegarde + '\\' + nomFicTemp + '.zip')
                         #Depassement de l'alphabet
                         if (ord(nomFicTemp[3]) > 122):
                              break

                    if not (exists(pathComplet)):
                        break
                    #Incrémenter le caractère courant
                    nomFicTemp =  nomFicTemp[:2] + chr(ord(nomFicTemp[2])+1) + nomFicTemp[3:]
                    #Reset la lettre suivante
                    nomFicTemp = nomFicTemp[:3] + 'A'
                    #Passer les caractères ASCCI que nous ne voulons pas
                    if (91 <= ord(nomFicTemp[2]) and ord(nomFicTemp[2]) <= 96):
                         nomFicTemp = nomFicTemp[:2] + 'a' + nomFicTemp[3:]
                    pathComplet = (pathSauvegarde + '\\' + nomFicTemp + '.zip')
                    if (ord(nomFicTemp[2]) > 122):
                         break

               if not (exists(pathComplet)):
                    break
               #Incrémenter le caractère courant
               nomFicTemp =  nomFicTemp[0] + chr(ord(nomFicTemp[1])+1) + nomFicTemp[2:]
               #Reset la lettre suivante
               nomFicTemp = nomFicTemp[:2] + 'A' + nomFicTemp[3:]
               #Passer les caractères ASCCI que nous ne voulons pas
               if (91 <= ord(nomFicTemp[1]) and ord(nomFicTemp[1]) <= 96):
                    nomFicTemp = nomFicTemp[0] + 'a' + nomFicTemp[2:]
               pathComplet = (pathSauvegarde + '\\' + nomFicTemp + '.zip')
               if (ord(nomFicTemp[1]) > 122):
                    break

          if not(exists(pathComplet)):
               break
          #Incrémenter le caractère courant
          nomFicTemp = chr(ord(nomFicTemp[0])+1) + nomFicTemp[1:]
          #Reset la lettre suivante
          nomFicTemp = nomFicTemp[0] + 'A' + nomFicTemp[2:]
          #Passer les caractères ASCCI que nous ne voulons pas
          if (91 <= ord(nomFicTemp[0]) and ord(nomFicTemp[0]) <= 96):
               nomFicTemp = 'a' + nomFicTemp[1:]
          pathComplet = (pathSauvegarde + '\\' + nomFicTemp + '.zip')
          if (ord(nomFicTemp[0]) > 122):
               break
     return nomFicTemp


class GestionPSR:
    def __init__(self, cheminEnregistrement):
        """
        Définit le chemin où les fichiers produits vont être enregistrées et le nom du fichier enregistré
        """
        self.nomFicTemp = genererNomFicTemp(cheminEnregistrement)
        self.sortieZip = r'{0}\{1}.zip'.format(cheminEnregistrement, self.nomFicTemp)
        self.__modifierConfig()

    def lancer(self):
        """
        Lance le logiciel PSR avec comme paramètres:
            /start : lancer PSR
            /arcxml 1 : produire un fichier de traces XML
            /sc 0 : ne pas faire de capture d'écran
            /gui 0 : cacher l'interface de PSR
            /output dossier de sortie des fichiers
        """
        Popen([pathPSR , "/start" , "/arcxml", "1" , "/sc", "0", "/gui", "0" , "/output" , self.sortieZip], shell=True)

    def arreter(self):
        """
        Arrête PSR
        """
        Popen([pathPSR , "/stop"],  shell=True)

    def __modifierConfig(self):
         """
         Enregistre les noms de fichiers produits par PSR dans le fichier de config
         """
         data["PSR"]["nomFicTempPSR"] = self.nomFicTemp
         file = open(pathConfig, 'w')
         file.write(dumps(data, indent=4))
         file.close()
