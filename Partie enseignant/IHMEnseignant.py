# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk,Button,Toplevel,filedialog
from lxml import etree

navigateurs = ["Firefox","Microsoft Edge","Internet Explorer","Google Chrome"]


menu = tk.Tk() #Création de la fenêtre pour commencer l'exercice
menu.filename = filedialog.askopenfilename(initialdir="./",title ="Choissisez un fichier",filetypes=[("Fichiers xml","*.xml")])
fichier = menu.filename

tree = etree.parse(fichier)
#menu.geometry("500x300")
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
heureDebut = tree.xpath("/Session/HeureDebut")
labelDebut = tk.Label(tabSynthese,text="Début de l'exercice :")
labelHeureDebut = tk.Label(tabSynthese,text=heureDebut[0].text+'.')

heureFin = tree.xpath("/Session/HeureFin")
tabHeureDebut = heureDebut[0].text.split(":")
tabHeureFin = heureFin[0].text.split(":")

dureeHeure = int(tabHeureFin[0]) - int(tabHeureDebut[0])
dureeMinute = int(tabHeureFin[1]) - int(tabHeureDebut[1])

dureeSeconde = int(tabHeureFin[2]) - int(tabHeureDebut[2])
if (dureeSeconde < 0):
    dureeMinute-=1
    dureeSeconde = 60 + dureeSeconde
if (dureeMinute < 0):
    dureeHeure-=1
    dureeMinute = 60 + dureeMinute

duree = str(dureeHeure)+":"+str(dureeMinute)+":"+str(dureeSeconde)
labelDuree = tk.Label(tabSynthese,text="Durée de l'exercice :")
labelDureeExo = tk.Label(tabSynthese,text=duree)

labelFin = tk.Label(tabSynthese,text="Fin de l'exercice :")
labelHeureFin = tk.Label(tabSynthese,text=heureFin[0].text)

logiciels = tree.find('Logiciels')
nomsLogiciel = logiciels.getchildren()
listeLogiciel = []
for i in range(len(nomsLogiciel)):
    listeLogiciel.append(nomsLogiciel[i].get("nom"))
stringLogiciels = ', '.join(listeLogiciel)+'.'
labelLogiciel = tk.Label(tabSynthese,text="Logiciels utilisés :")
labelListeLogiciel = tk.Label(tabSynthese,text=stringLogiciels)


labelPremierLogiciel = tk.Label(tabSynthese,text="Premier logiciel utilisé :")
labelNomPremierLogiciel = tk.Label(tabSynthese,text=listeLogiciel[0]+'.')

actions = tree.find(".//Actions")
premiereAction = actions[0].getchildren()
labelPremiereAction = tk.Label(tabSynthese,text="Premiere action faite :")
labelNomPremiereAction = tk.Label(tabSynthese,text=premiereAction[1].text)
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

for i in range(len(listeLogiciel)):
    enfantLogiciel = nomsLogiciel[i].getchildren()
    duree = enfantLogiciel[1].text
    tab.insert("","end",None,text=listeLogiciel[i], values=(duree,enfantLogiciel[0].text))



tab.pack(side=tk.TOP,fill=tk.X)

"""
ONGLET INTERROGATION
"""

typeRecherche = ["Nombre de"]
typeRechercheNav = []
for i in range(len(typeRecherche)):
    typeRechercheNav.append(typeRecherche[i])
typeRechercheNav.append("Liste des")
tabInterro = ttk.Treeview(tabInterrogation)
tabInterro["columns"]=()
tabInterro.column("#0",width=1000,minwidth=100)
tabInterro.heading("#0",text="")

tabInterro.grid(sticky="W",row=2,column=0,columnspan=6,padx=15,pady=5)

def rechercher():
    labelReponse['text']=""
    for i in tabInterro.get_children():
        tabInterro.delete(i)
    tabInterro.heading("#0",text='')
    
    if(comboInfo1.current()!=-1):
        if(comboInfo1.get()=="Nombre de"):
            nbActions = 0
            logicielChoisi = nomsLogiciel[comboLogiciel.current()]
            contenuLogiciel = logicielChoisi.getchildren()
            lesActions = contenuLogiciel[2].getchildren()
            for i in range(len(lesActions)):
                if (lesActions[i].get('nom') == comboInfo2.get()):
                    nbActions += 1
            if(nbActions > 1):
                labelReponse['text'] = "L'étudiant a effectué "+str(nbActions)+" "+str(comboInfo2.get()).lower()+"s"
            else:
                labelReponse['text'] = "L'étudiant a effectué "+str(nbActions)+" "+str(comboInfo2.get()).lower()
            if(comboInfo2.get()=="Page visité"):
                listeRecherche = []
                logicielChoisi = nomsLogiciel[comboLogiciel.current()]
                contenuLogiciel = logicielChoisi.getchildren()
                lesActions = contenuLogiciel[2].getchildren()
                for i in range(len(lesActions)-1):    
                    contenuAction = lesActions[i].getchildren()
                    for i in range (len(contenuAction)):
                        if (contenuAction[i].tag=="NomPage" and contenuAction[3].text is not None):
                            if(comboLogiciel.get()=="Google Chrome"):
                                tabSite = contenuAction[3].text.split("- Google Chrome")
                            if(comboLogiciel.get()=="Internet Explorer"):
                                tabSite = contenuAction[3].text.split("- Internet Explorer")
                            if(comboLogiciel.get()=="Firefox"):
                                tabSite = contenuAction[3].text.split("- Mozilla Firefox")
                    if(tabSite[0] not in listeRecherche):
                        listeRecherche.append(tabSite[0])
                if(len(listeRecherche) > 1):
                    labelReponse['text'] = "L'étudiant a visité "+str(len(listeRecherche))+" pages"
                else:
                    labelReponse['text'] = "L'étudiant a visité "+str(len(listeRecherche))+" page"
        if(comboInfo1.get()=="Liste des"):
            if(comboInfo2.get()=="Page visité"):
                tabInterro.heading("#0",text="Nom de la page")
                listeRecherche = []
                logicielChoisi = nomsLogiciel[comboLogiciel.current()]
                contenuLogiciel = logicielChoisi.getchildren()
                lesActions = contenuLogiciel[2].getchildren()
                for i in range(len(lesActions)-1):    
                    contenuAction = lesActions[i].getchildren()
                    for i in range (len(contenuAction)):
                        if (contenuAction[i].tag=="NomPage" and contenuAction[3].text is not None):
                            if(comboLogiciel.get()=="Google Chrome"):
                                tabSite = contenuAction[3].text.split("- Google Chrome")
                    if(tabSite[0] not in listeRecherche):
                        listeRecherche.append(tabSite[0])
                
                for page in listeRecherche:
                    tabInterro.insert("","end",None,text=page, values=())                                
        

labelLogiciel = tk.Label(tabInterrogation,text="Logiciel :")
comboLogiciel = ttk.Combobox(tabInterrogation,state="readonly", values=listeLogiciel)

labelLogiciel.grid(sticky="W",row=0,column=0,padx=15,pady=5)
comboLogiciel.grid(sticky="W",row=0,column=1,pady=5)

labelInfo = tk.Label(tabInterrogation,text="Types d'informations :")
comboInfo1 = ttk.Combobox(tabInterrogation,state="readonly", values=typeRecherche)
comboInfo1.configure(state="disabled")
comboInfo2 = ttk.Combobox(tabInterrogation,state="readonly")
comboInfo2.configure(state="disabled")
        

labelInfo.grid(sticky="W",row=0,column=2,padx=15,pady=5)
comboInfo1.grid(sticky="W",row=0,column=3,pady=5)
comboInfo2.grid(sticky="W",row=0,column=4,padx = 15,pady=5)

boutonRechercher = Button(tabInterrogation,text="Rechercher", command=rechercher)
boutonRechercher.grid(sticky="W",row=0,column=5,padx = 15,pady=5)

labelReponse = tk.Label(tabInterrogation,text="")
labelReponse.grid(sticky="W",row=1,column=0,columnspan=5,padx=15,pady=5)
        

"""
ONGLET REPLAY
"""
labelReplay = tk.Label(tabReplay,text="Ceci est l'onglet du replay")
labelReplay.pack()





def infomationsLogiciel(logiciel):
    enfants = logiciel.getchildren()
    lesActions = enfants[2].getchildren()
    """
    Informations générales d'un logiciel
    """
    fenetreInformations = Toplevel()
    fenetreInformations.geometry("700x300")
    fenetreInformations.title("Informations - " + logiciel.get('nom'))
    lblNomLogiciel = tk.Label(fenetreInformations,text=logiciel.get('nom')).pack()
    lblHeureOuverture = tk.Label(fenetreInformations,text="Heure d'ouverture : " + enfants[0].text).pack()
    lblDureeOuvert = tk.Label(fenetreInformations,text="Temps d'utilisation : " + enfants[1].text).pack()
    tabOuverture = enfants[0].text.split(':')
    tabDuree = enfants[1].text.split(':')
    dureeHeure = int(tabOuverture[0])+int(tabDuree[0])
    dureeMinute = int(tabOuverture[1])+int(tabDuree[1])
    dureeSeconde = int(tabOuverture[2])+int(tabDuree[2])
    
    if (dureeSeconde > 60):
        dureeMinute+=1
        dureeSeconde-=60
    if (dureeMinute > 60):
        dureeHeure+=1
        dureeMinute-=60
    duree = str(dureeHeure)+":"+str(dureeMinute)+":"+str(dureeSeconde)
    lblFinLogiciel = tk.Label(fenetreInformations,text="Heure de fermeture : "+duree).pack()

    """
    Tableau d'actions d'un logiciel
    """
    tabActions = ttk.Treeview(fenetreInformations)
    tabActions["columns"]=("un","deux","trois","quatre")
    tabActions.column("#0",width=70,minwidth=50)
    tabActions.column("un",width=100,minwidth=100)
    tabActions.column("deux",width=100,minwidth=100)
    tabActions.column("trois",width=100,minwidth=100)
    tabActions.column("quatre",width=100,minwidth=100)

    
    tabActions.heading("#0",text="TypeAction",anchor=tk.W)
    tabActions.heading("un",text="Description",anchor=tk.W)
    tabActions.heading("deux",text="Heure",anchor=tk.W)
    tabActions.heading("trois",text="Nom de la page",anchor=tk.W)
    tabActions.heading("quatre",text="Saisie",anchor=tk.W)

    for i in range(len(lesActions)):
        uneAction = lesActions[i].getchildren()
        description = deEmojify(str(uneAction[1].text))
        hDebut = str(uneAction[2].text)
        nomPage = deEmojify(str(uneAction[3].text))
        if (len(uneAction)==4):
            tabActions.insert("","end",None,text=lesActions[i].get("nom"), values=(description,hDebut,nomPage,""))
            
        else:
            saisie = str(uneAction[4].text)
            tabActions.insert("","end",None,text=lesActions[i].get("nom"), values=(description,hDebut,nomPage,saisie))


    
    tabActions.pack(side=tk.TOP,fill=tk.X)

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')


def choixInfo2(evt):
    remplirComboBox(evt)
    if comboInfo1.get()=="Liste des":
        comboInfo2['values'] = ["Page visité"]


def remplirComboBox(evt):
    if(comboLogiciel.current()!=-1):
        logicielChoisi = nomsLogiciel[comboLogiciel.current()]
        contenuLogiciel = logicielChoisi.getchildren()
        lesActions = contenuLogiciel[2].getchildren()
        typesAction = []
        for i in range(len(lesActions)):
            if lesActions[i].get('nom') not in typesAction:
                typesAction.append(lesActions[i].get('nom'))
        typeActionNav = []
        for i in range(len(typesAction)):
            typeActionNav.append(typesAction[i])
        typeActionNav.append("Page visité")
        comboInfo2['values']=typesAction
        comboInfo1.configure(state="readonly")
        comboInfo2.configure(state="readonly")

        if(comboLogiciel.get()in navigateurs):
            comboInfo1['values'] = typeRechercheNav
            comboInfo2['values'] = typeActionNav
        else:
            comboInfo1['values'] = typeRecherche
            comboInfo2['values'] = typesAction
    if(comboLogiciel.current()==-1):
        comboInfo1.configure(state="disabled")
        comboInfo2.configure(state="disabled")


def onClick(evt):
    if(tab_parent.index(tab_parent.select()) == 1 and evt.y >= 26):
        cy=evt.y-26
        index = int(cy/19)
        infomationsLogiciel(nomsLogiciel[index])

    
menu.bind("<Button 1>",onClick)
comboLogiciel.bind("<<ComboboxSelected>>",remplirComboBox)
comboInfo1.bind("<<ComboboxSelected>>",choixInfo2)
tab_parent.pack(expand=1,fill='both')
menu.mainloop()
