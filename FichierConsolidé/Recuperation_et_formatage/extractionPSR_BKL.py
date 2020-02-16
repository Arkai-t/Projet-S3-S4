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
    attrSession = session.items()
    i = 0
    for attribut in attrSession:
        
        print("Attribut session "+ str(i)+" : ")

        print ("   "+str(attrSession[i][0]))
        print ("   "+str(attrSession[i][1]))
        i+= 1
   
    for action in tree.xpath("/Report/UserActionData/RecordSession/EachAction"):
        print("\n")
        attrAction = action.items()
        k = 0
        l = 1
        for attribut in attrAction:
            if str(attrAction[k][0]) == "ProgramId" or str(attrAction[k][0]) == "FileId" or str(attrAction[k][0]) == "FileVersion" or str(attrAction[k][0]) == "FileCompany" or str(attrAction[k][0]) == "CommandLine": 
                l -= 1
            else: 
                print("Attribut action "+ str(l)+" : ")
                print (attrAction[k][0])
                print (attrAction[k][1])
            print("\n")    
            k+= 1
            l += 1
            
   
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
                            print("   Attribut "+ str(j)+" : ")
                            print ("                "+str(attrUIAStack[j][0]))
                            if attrUIAStack[j][0] == "BoundingRectangle":
                                s = str(attrUIAStack[j][1]);
                                l = s.split(',');
                                for i in range(0,len(l)):
                                    print("                 "+str(l[i]));
                                    
                                
                            else:
                                print ("                 "+str(attrUIAStack[j][1]))
                            j+= 1
                        print("\n")    
                                            
                   
                      
                
                
                print(enfant.text)
                print("\n")
        
        
        
                
      
