# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 22:45:00 2020
@author: paul6
"""


#RIEN N'EST FINI ICI ! TOUTE LA PARTIE D'AJOUT EST ENCORE A FAIRE

from lxml import etree
from TraitementBasicKeyLogger import BKLtoTxt
from TraitementBasicKeyLogger import Mot


def heureToNb(heure):
    (h, m, s) = heure.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

conversion = BKLtoTxt('kpc_log.tsv')

tableauMots = conversion.recupererPhrases()

tableauActionsTxt = []


tree = etree.parse("testBKL_PSR.xml")

root = tree.getroot()
etree.tostring(root)

for texteAction in root.xpath('/Report/UserActionData/RecordSession/EachAction/Action/text()'):
    #print(action)
    if texteAction == "Saisie au clavier":
        parent = texteAction.getparent().getparent() #Balise EachAction associée
        
        action = texteAction.getParent()
        
        debutActionPSR = parent.get("Time")
        
        for mot in tableauMots:
            if not (heureToNb(mot.getHeureDebut()) < heureToNb(debutActionPSR) and heureToNb(mot.getHeureFin()) > heureToNb(debutActionPSR)):
                print("Ajouter le texte au BKL")
            
            
                baliseTxt = etree.Element("texte")
                baliseTxt.set("heureDebut", mot.getHeureDebut())
                baliseTxt.set("heureFin", mot.getHeureFin())
                baliseTxt.text = mot.getMot()

                action.insert(action.index("Action")+1, baliseTxt)
                
                print(etree.tostring(baliseTxt), " inséré")
        

