# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk,Button

fichierLabel = open("InfosLabel.txt",'r')

menu = tk.Tk() #Création de la fenêtre pour commencer l'exercice
menu.geometry("500x300")
menu.title("Système d'analyse de traces - Enseignant")
tab_parent = ttk.Notebook(menu)

#Création des différents onglets
tabSynthese = ttk.Frame(tab_parent)
tabActivite = ttk.Frame(tab_parent)
tabInterrogation = ttk.Frame(tab_parent)
tabReplay = ttk.Frame(tab_parent)

#ajout des onglets dans la fenêtre principale
tab_parent.add(tabSynthese,text="Synthèse")
tab_parent.add(tabActivite,text="Activité")
tab_parent.add(tabInterrogation,text="Interrogation")
tab_parent.add(tabReplay,text="Replay")

"""
ONGLET SYNTHESE
Ajout des éléments
"""
labelDebut = tk.Label(tabSynthese,text="Début de l'exercice :")
labelHeureDebut = tk.Label(tabSynthese,text=fichierLabel.readline())

labelDuree = tk.Label(tabSynthese,text="Durée de l'exercice :")
labelDureeExo = tk.Label(tabSynthese,text=fichierLabel.readline())

labelFin = tk.Label(tabSynthese,text="Fin de l'exercice :")
labelHeureFin = tk.Label(tabSynthese,text=fichierLabel.readline())

labelLogiciel = tk.Label(tabSynthese,text="Logiciels utilisés :")
labelListeLogiciel = tk.Label(tabSynthese,text=fichierLabel.readline())

labelPremierLogiciel = tk.Label(tabSynthese,text="Premier logiciel utilisé :")
labelNomPremierLogiciel = tk.Label(tabSynthese,text=fichierLabel.readline())

labelPremiereAction = tk.Label(tabSynthese,text="Premiere action faite :")
labelNomPremiereAction = tk.Label(tabSynthese,text=fichierLabel.readline())
"""
Placement des éléments
"""
labelDebut.grid(sticky="W",row=0,column=0,padx=15,pady=5)
labelHeureDebut.grid(sticky="W",row=0,column=1,pady=5)

labelDuree.grid(sticky="W",row=1,column=0,padx=15,pady=5)
labelDureeExo.grid(sticky="W",row=1,column=1,pady=5)

labelFin.grid(sticky="W",row=2,column=0,padx=15,pady=5)
labelHeureFin.grid(sticky="W",row=2,column=1,pady=5)

labelLogiciel.grid(sticky="W",row=3,column=0,padx=15,pady=5)
labelListeLogiciel.grid(sticky="W",row=3,column=1,pady=5)

labelPremierLogiciel.grid(sticky="W",row=4,column=0,padx=15,pady=5)
labelNomPremierLogiciel.grid(sticky="W",row=4,column=1,pady=5)

labelPremiereAction.grid(sticky="W",row=5,column=0,padx=15,pady=5)
labelNomPremiereAction.grid(sticky="W",row=5,column=1,pady=5)
"""
ONGLET ACTIVITE
"""
tab = ttk.Treeview(tabActivite)
tab["columns"]=("un","deux")
tab.column("#0",width=100,minwidth=100)
tab.column("un",width=100,minwidth=100)
tab.column("deux",width=100,minwidth=100)

tab.heading("#0",text="Nom du logiciel",anchor=tk.W)
tab.heading("un",text="Durée d'utilisation",anchor=tk.W)
tab.heading("deux",text="Heure de lancement",anchor=tk.W)

tab.insert("","end",None,text="Mozilla Firefox", values=("30 min 57 sec","15:15"))
tab.insert("","end",None,text="R Studio", values=("59 min 23 sec","15:45"))
tab.insert("","end",None,text="CodeBlocks", values=("43 min 20 sec","15:56"))
tab.insert("","end",None,text="Google Chrome", values=("1 h 10 min 20 sec","15:15"))


tab.pack(side=tk.TOP,fill=tk.X)

"""
ONGLET INTERROGATION
"""

labelLogiciel = tk.Label(tabInterrogation,text="Logiciel :")
comboLogiciel = ttk.Combobox(tabInterrogation,values=["Tous","a","b","c"])

labelLogiciel.grid(sticky="W",row=0,column=0,padx=15,pady=5)
comboLogiciel.grid(sticky="W",row=0,column=1,pady=5)

labelInfo = tk.Label(tabInterrogation,text="Types d'informations :")
comboInfo1 = ttk.Combobox(tabInterrogation,values=["Tous","a","b","c"])
comboInfo2 = ttk.Combobox(tabInterrogation,values=["Tous","a","b","c"])

labelInfo.grid(sticky="W",row=0,column=2,padx=15,pady=5)
comboInfo1.grid(sticky="W",row=0,column=3,pady=5)
comboInfo2.grid(sticky="W",row=0,column=4,padx = 15,pady=5)

boutonRechercher = Button(tabInterrogation,text="Rechercher")
boutonRechercher.grid(sticky="W",row=0,column=5,padx = 15,pady=5)


"""
ONGLET REPLAY
"""
labelReplay = tk.Label(tabReplay,text="Ceci est l'onglet du replay")
labelReplay.pack()

tab_parent.pack(expand=1,fill='both')
menu.mainloop()
