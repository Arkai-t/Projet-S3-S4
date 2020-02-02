# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 22:45:00 2020

@author: paul6
"""


#RIEN N'EST FINI ICI ! TOUTE LA PARTIE D'AJOUT EST ENCORE A FAIRE

from lxml import etree
from TraitementBasicKeyLogger import BKLtoTxt
from TraitementBasicKeyLogger import Mot

conversion = BKLtoTxt('kpc_log.tsv')

tableauMots = conversion.recupererPhrases()

tableauActionsTxt = []


tree = etree.parse("testing.xml")

root = tree.getroot()
etree.tostring(root)

for action in root.xpath('/Report/UserActionData/RecordSession/EachAction/Action/[text()'):
    #print(action)
    if action == "Saisie au clavier":
        parent = action.getparent().getparent() #Balise EachAction associée
        debutActionPSR = parent.get("Time")
        
        for mot in tableauMots:
            if(mot.getHeureDebut() < debutActionPSR or mot.getHeureFin() > debutActionPSR):
                break
            
            print("Ajouter le texte au BKL")
            
                
        
        
    
        #tableauActionsTxt.append(parent)
        
        #baliseTxt = etree.Element("texte")
        
        #parent.insert(parent.index(name)+1, etree.XML('<name>testage</name>'))