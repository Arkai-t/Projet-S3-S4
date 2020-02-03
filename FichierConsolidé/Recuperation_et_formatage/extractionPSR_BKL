# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 13:07:46 2020

@author: Malo
"""

import os
from lxml import etree
from RecuperationDonneesPSR_BKL import RecuperationDonneesPSR_BKL
from FormatageDonneesPSR_BKL import FormatageDonneesPSR_BKL


#root = etree.parse(r'leTestXml.xml')
#print etree.tostring(root)

tree = etree.parse("leTestXml.xml")
for action in tree.xpath("/Report/UserActionData/RecordSession/EachAction"):
    print("Logiciel :"+ action.get("FileDescription"))
    print("\n")
    
    enfants = action.getchildren()
    for enfant in enfants: 
        if enfant.tag != "CursorCoordsXY" and enfant.tag != "ScreenCoordsXYWH" and enfant.tag != "ScreenshotFileName":
            print(enfant.tag)
            print(" = ")
            print(enfant.text)
            print("\n")
  
    #print("Description : ")
    #print (tree.xpath("/Report/UserActionData/RecordSession/EachAction/Description/text()"))
    

    
