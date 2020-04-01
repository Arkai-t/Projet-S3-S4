#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 10:32:50 2020

@author: malo, esteban

Objectif : recuprer les données de saisies dans le fichier consolidé, ouvrir word et écrire les données de saisie dans word
"""

#import des modules nessécaires et déclarations initiales
from pywinauto.application import Application
from lxml import etree
import time
nomlogiciel = "Bloc-notes"
fichierConsolidé = "aaaa_FichierConsolide.xml"
tabSaisie = [] # creation d'un tableau de stockage des saisie a esnuite afficher
nomFichierNotePad = "bbbb.txt"


# /// récuparation des saisies dans le 

tree = etree.parse(fichierConsolidé)

session = tree.xpath("Logiciels")
    
for logiciel in session[0].getchildren():
    attributsLogicielCourant = logiciel.items()
    if attributsLogicielCourant[0][1] == nomlogiciel: # si le logiciel courant est google chrome
        # déterminer ses enfants 
        balisesLogiciel = logiciel.getchildren()
        # parcourrir les enfants
        for balise in balisesLogiciel:
            # si l'enfant est actions
            if balise.tag == 'Actions':
                # determiner ses enfants (les actions)
                actions = balise.getchildren()
                # parcourir les enfants
                for action in actions:
                    attributActionCourante = action.getchildren()
                    # verifier le type de chaque action courante
                    for typeAction in attributActionCourante:
                        if typeAction.tag == 'Saisie': #si l'action est de type 'saisie'
                            # on récupère ses enfants
                            #print(typeAction.text)
                            tabSaisie.append(typeAction.text)
                            
                   
                    
# ///  exploitation                            
                    
app = Application().start("notepad.exe")
for saisie in tabSaisie:
    #app.UntitledNotepad.Edit.type_keys("pywinauto marche!", with_spaces = True)
    app.UntitledNotepad.Edit.type_keys(saisie, with_spaces = True)
    app.UntitledNotepad.Edit.type_keys('{ENTER}', with_spaces = True)
#sauvegarde du fichier 
time.sleep(1)    
app.Notepad.menu_select("Fichier ->Enregistrer sous")    
app.dialog.Edit.SetText(nomFichierNotePad)
app.dialog.EnregistrerButton.Click()

                                   
        

