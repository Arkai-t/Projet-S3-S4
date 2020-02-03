# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 18:26:49 2020

@author: Malo
"""

import os
from lxml import etree

class RecuperationDonnees:
    """
    Classe qui permet de récupérer les données récoltées de PSR et BLK.
    Elle récupére les données d'un fichier PSR 
    lui même consolidé par les données essentielles du BLK (horodatage et contenu du texte)
    """
    # attributs
    
    # méthodes
    
    def __init__():
        root = etree.parse(r"leTestXml.xml")
        print etree.tostring(root)
    

