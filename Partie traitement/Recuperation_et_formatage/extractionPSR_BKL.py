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

print("---------------------------------------------------------------------")
#creation de la liste de logiciels
listeDeLogiciels = []
listeDeLogiciels.append(3)
print(len(listeDeLogiciels))
#creation du dictionnaire regroupant les informations des sessions
infoSession = {}

#parssage du fichier XML
tree = etree.parse("leTestXml.xml")

for session in  tree.xpath("/Report/UserActionData/RecordSession"): #on se positionne au niveau de la balise <RecordSession>
    attrSession = session.items() 
    
    #affichage des attribus de la balise <RecordSession>
    for attribut in attrSession: 
        print("Attribut session "+" : ")
        #print ("   "+str(attrSession[i][0]))
        #print ("   "+str(attrSession[i][1]))
        clefSession = attribut[0]
        valueSession = attribut[1]
        infoSession[clefSession] = valueSession
        print (attribut[0])
        print(infoSession[attribut[0]])        
    
    
    
    for action in tree.xpath("/Report/UserActionData/RecordSession/EachAction"):#on se positionne au niveau de la balise <EachAction>
        print("\n")
        attrAction = action.items()
        
        l = 1
        
        for attribut in attrAction:
            
            #for i in range(0,len(listeDeLogiciels)):
               # print('')
            if str(attribut[0]) == "ProgramId" or str(attribut[0]) == "FileId" or str(attribut[0]) == "FileVersion" or str(attribut[0]) == "FileCompany" or str(attribut[0]) == "CommandLine": 
                l -= 1
            else: 
                print("Attribut action "+ str(l)+" : ")
                print (attribut[0])
                print (attribut[1])
            print("\n")
            l += 1
            #creation du dico action
            #for i in range (0,len(listeDeLogiciels)):
             #   if attrAction[k][0] == listeDeLogiciels[i]:
              #      print('')
                    
   
        enfants = action.getchildren()
        for enfant in enfants: 
            if enfant.tag != "CursorCoordsXY" and enfant.tag != "ScreenCoordsXYWH" and enfant.tag != "ScreenshotFileName":
                print(enfant.tag+" : ")
                print(enfant.text)
                if enfant.tag == "UIAStack":
                    #récupérer tous les attributs de la balise UIAStack
                    enfantsDeUIAStack = enfant.getchildren()
                    
                    for enfantUIAStack in enfantsDeUIAStack :
                        print(enfantUIAStack.tag+" : ")
                        attrUIAStack = enfantUIAStack.items()
                        
                        for attribut in attrUIAStack:
                            print("   Attribut "+ str(j)+" : ")
                            print ("                "+str(attribut[0]))
                            if attribut[0] == "BoundingRectangle":
                                s = str(attribut[1]);
                                l = s.split(',');
                                for i in range(0,len(l)):
                                    print("                 "+str(l[i]));
                                    
                                
                            else:
                                print ("                 "+str(attribut[1]))
                        print("\n")  
                print("\n")
        
print(infoSession)        
        
#embouteillage des données dans une liste (logiciels) de dictionnaires
                #pour chaque balise EachAction : prendre (nom du logiciel, description, action, contenu de UIASTACK et texte )
                
#affichage de la liste d'action                
