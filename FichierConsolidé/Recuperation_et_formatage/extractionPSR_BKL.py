# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 13:07:46 2020

@author: Malo
"""

#import os #pas utilisée
from lxml import etree
#from RecuperationDonneesPSR_BKL import RecuperationDonneesPSR_BKL
#from FormatageDonneesPSR_BKL import FormatageDonneesPSR_BKL


#root = etree.parse(r'leTestXml.xml')
#print etree.tostring(root)

tree = etree.parse("leTestXml.xml")

for session in  tree.xpath("/Report/UserActionData/RecordSession"):
    AttrSession = session.items()
    i = 0
    for attribut in AttrSession:
        
        print("attribut "+ str(i)+" : ")
        print (AttrSession[i])
        i+= 1
   
    for action in tree.xpath("/Report/UserActionData/RecordSession/EachAction"):
        print("\n")
        print (action.items())
        #print("Logiciel :"+ action.get("FileDescription"))
        #print("\n")
        
        enfants = action.getchildren()
        for enfant in enfants: 
            if enfant.tag != "CursorCoordsXY" and enfant.tag != "ScreenCoordsXYWH" and enfant.tag != "ScreenshotFileName":
                print(enfant.tag+" : ")
                if enfant.tag == "UIAStack":
                    print("\n")   
                    #récupérer tous les attributs de la balise UIAStack
                    enfantsDeUIAStack = enfant.getchildren()
                    for enfantUIAStack in enfantsDeUIAStack :
                        print(enfantUIAStack.tag+" : ")
                        attrUIAStack = enfantUIAStack.items()
                        j = 0
                        for attribut in attrUIAStack:
                            print("   attribut "+ str(j)+" : ")
                            print ("     "+str(attrUIAStack[j]))
                            j+= 1
                        print("\n")    
                                            
                   
                      
                
                
                print(enfant.text)
                print("\n")
                
                    
                
      
        #print("Description : ")
        #print (tree.xpath("/Report/UserActionData/RecordSession/EachAction/Description/text()"))
        
