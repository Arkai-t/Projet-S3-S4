# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 22:45:00 2020
@author: paul6
"""


from lxml import etree
from TraitementBasicKeyLogger import BKLtoTxt



def heureToNb(heure): #string sous forme de date en nb
    (h, m, s) = heure.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

 #Conversion tsv en objets mot
conversion = BKLtoTxt('kpcd_log.tsv')
tableauMots = conversion.recupererPhrases()

 #initialisation du xml
tree = etree.parse("test.xml") 
root = tree.getroot()
etree.tostring(root)


for texteAction in root.xpath('/Report/UserActionData/RecordSession/EachAction/Action/text()'):
    if texteAction == "Saisie au clavier":
        parent = texteAction.getparent().getparent() #Balise EachAction de l'action récupérée
        
        action = texteAction.getparent() #Balise action en elle meme
        
        #temp de debut de l'action et fin (debut de la suivante)
        debutActionPSR = parent.get("Time")
        parentSuivant = parent.getnext()
        nextActionPSR = parentSuivant.get("Time")
        
        
        for mot in tableauMots:
            if (heureToNb(mot.getHeureDebut()) >= heureToNb(debutActionPSR) and (heureToNb(mot.getHeureFin()) <= heureToNb(nextActionPSR))):
                
                #creation de l'element de texte
                baliseTxt = etree.Element("texte")
                baliseTxt.set("heureDebut", mot.getHeureDebut())
                baliseTxt.set("heureFin", mot.getHeureFin())
                baliseTxt.text = mot.getMot()

                parent.insert(parent.index(action)+1, baliseTxt) #insertion après l'action
                
#enregistrement de l'xml modifié
etree.ElementTree(root).write("xmlModifie.xml", pretty_print = True, xml_declaration=True, encoding="utf-8")
