# -*- coding: utf-8 -*-
from sys import exit
import tkinter as tk
from tkinter import ttk,Button,Toplevel,filedialog,messagebox
from lxml import etree

navigateurs = ["Firefox","Microsoft Edge","Internet Explorer","Google Chrome"]


menu = tk.Tk() #Création de la fenêtre pour commencer l'exercice
menu.filename = filedialog.askopenfilename(initialdir="./",title ="Choissisez un fichier",filetypes=[("Fichiers xml","*.xml")]) #Menu permettant de choisir un fichier
fichier = menu.filename

#Si le fichier est vide, afficher une erreur et fermer le programme
if(fichier==""):
    messagebox.showinfo("Erreur","Aucun fichier n'a été choisi")
    menu.destroy()
    exit()
tree = etree.parse(fichier)

racine = tree.getroot()
#Si le fichier n'est pas correctement structuré, afficher une erreur et fermer le programme

if racine.find('Logiciels/Logiciel/Actions/Action/TypeAction') is None:
    messagebox.showinfo("Erreur","Le fichier choisi n'est pas correctement structuré")
    menu.destroy()
    exit()

#Paramétrage de la fenêtre
menu.minsize(900,350)
menu.resizable(False,False)
menu.title("Système d'analyse de traces - Enseignant")

#Création du "Notebook" (menu avec les différents onglets)
tab_parent = ttk.Notebook(menu)

#Création des différents onglets
tabSynthese = ttk.Frame(tab_parent)
tabActivite = ttk.Frame(tab_parent)
tabInterrogation = ttk.Frame(tab_parent)

#ajout des onglets dans la fenêtre principale
tab_parent.add(tabSynthese,text="Synthèse")
tab_parent.add(tabActivite,text="Activité")
tab_parent.add(tabInterrogation,text="Interrogation")

"""
ONGLET SYNTHESE
Ajout des éléments
"""
#Recherche de l'heure de début de l'exercice
heureDebut = tree.xpath("/Session/HeureDebut")
labelDebut = tk.Label(tabSynthese,text="Début de l'exercice :")
#Affichage de l'heure de début dans un label
labelHeureDebut = tk.Label(tabSynthese,text=heureDebut[0].text)

#Recherche de l'heure de fin de l'exercice
heureFin = tree.xpath("/Session/HeureFin")
#Décomposition des heures dans deux tableaux
tabHeureDebut = heureDebut[0].text.split(":")
tabHeureFin = heureFin[0].text.split(":")
#Calcul de la durée de l'exercice
dureeHeure = int(tabHeureFin[0]) - int(tabHeureDebut[0])
dureeMinute = int(tabHeureFin[1]) - int(tabHeureDebut[1])
dureeSeconde = int(tabHeureFin[2]) - int(tabHeureDebut[2])
if (dureeSeconde < 0):
    dureeMinute-=1
    dureeSeconde = 60 + dureeSeconde
if (dureeMinute < 0):
    dureeHeure-=1
    dureeMinute = 60 + dureeMinute
#Mise en place de la durée en chaine de caractères
duree = str(dureeHeure)+":"+str(dureeMinute)+":"+str(dureeSeconde)
labelDuree = tk.Label(tabSynthese,text="Durée de l'exercice :")
#Affichage de la durée de l'exercice dans un label
labelDureeExo = tk.Label(tabSynthese,text=duree)

labelFin = tk.Label(tabSynthese,text="Fin de l'exercice :")
#Affichage de l'heure de fin dans un label
labelHeureFin = tk.Label(tabSynthese,text=heureFin[0].text)

#Recherche des différents logiciels
logiciels = tree.find('Logiciels')
#Récupération de la balise contenant les noms des logiciels
nomsLogiciel = logiciels.getchildren()
listeLogiciel = []
for i in range(len(nomsLogiciel)):
    #Ajout des noms de logiciels dans un tableau
    listeLogiciel.append(nomsLogiciel[i].get("nom"))
#Mise en place des noms des logiciels dans une chaine de caractères
stringLogiciels = ', '.join(listeLogiciel)+'.'
labelLogiciel = tk.Label(tabSynthese,text="Logiciels utilisés :")
#Affichage des logiciels dans un label
labelListeLogiciel = tk.Label(tabSynthese,text=stringLogiciels)


labelPremierLogiciel = tk.Label(tabSynthese,text="Premier logiciel utilisé :")
#Affichage du premier logiciel utilisé dans un label
labelNomPremierLogiciel = tk.Label(tabSynthese,text=listeLogiciel[0]+'.')

#Récupération des actions effectuées
actions = tree.find(".//Actions")
#Récupèration des balises fille de la première action
premiereAction = actions[0].getchildren()
labelPremiereAction = tk.Label(tabSynthese,text="Premiere action faite :")
#Affichage de la première action dans un label
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
#Création du tableau
tab = ttk.Treeview(tabActivite)
tab["columns"]=("un","deux")
tab.column("#0",width=100,minwidth=100)
tab.column("un",width=100,minwidth=100)
tab.column("deux",width=100,minwidth=100)

#Définition du nom des colonnes du tableau
tab.heading("#0",text="Nom du logiciel",anchor=tk.W)
tab.heading("un",text="Durée d'utilisation",anchor=tk.W)
tab.heading("deux",text="Heure de lancement",anchor=tk.W)

#Remplissage du tableau
for i in range(len(listeLogiciel)):
    #Récupération du logiciel
    enfantLogiciel = nomsLogiciel[i].getchildren()
    duree = enfantLogiciel[1].text
    #Insertion dans le tableau
    tab.insert("","end",None,text=listeLogiciel[i], values=(duree,enfantLogiciel[0].text))



tab.pack(side=tk.TOP,fill=tk.X)

"""
ONGLET INTERROGATION
"""

#Définition des types de recherche
typeRecherche = ["Nombre de"]
typeRechercheNav = []
for i in range(len(typeRecherche)):
    typeRechercheNav.append(typeRecherche[i])
typeRechercheNav.append("Liste des")
#Création du tableau 
tabInterro = ttk.Treeview(tabInterrogation)
tabInterro["columns"]=()
tabInterro.column("#0",width=1000,minwidth=100)
tabInterro.heading("#0",text="")

tabInterro.grid(sticky="W",row=2,column=0,columnspan=6,padx=15,pady=5)

def rechercher():
    #Vider le label de réponse
    labelReponse['text']=""
    #vider le tableau de réponse
    for i in tabInterro.get_children():
        tabInterro.delete(i)
    tabInterro.heading("#0",text='')
    #Vérification que quelque chose a été sélectionné
    if(comboInfo1.current()!=-1):
        
        if(comboInfo1.get()=="Nombre de"):
            nbActions = 0
            logicielChoisi = nomsLogiciel[comboLogiciel.current()]
            contenuLogiciel = logicielChoisi.getchildren()
            lesActions = contenuLogiciel[2].getchildren()
            for i in range(len(lesActions)):
                #Compter le nombre de fois un type d'action apparaît pour un logiciel
                if (lesActions[i].get('nom') == comboInfo2.get()):
                    nbActions += 1
            #Affichage de la réponse
            if(nbActions > 1):
                labelReponse['text'] = "L'étudiant a effectué "+str(nbActions)+" "+str(comboInfo2.get()).lower()+"s"
            else:
                labelReponse['text'] = "L'étudiant a effectué "+str(nbActions)+" "+str(comboInfo2.get()).lower()
            if(comboInfo2.get()=="Pages visités"):
                listeRecherche = []
                #Récupération d'un logiciel et de son contenu
                logicielChoisi = nomsLogiciel[comboLogiciel.current()]
                contenuLogiciel = logicielChoisi.getchildren()
                lesActions = contenuLogiciel[2].getchildren()
                for i in range(len(lesActions)-1):
                    #Récupération du contenu de la i-ème action
                    contenuAction = lesActions[i].getchildren()
                    for i in range (len(contenuAction)):
                        #Récupération de la page visité
                        if (contenuAction[i].tag=="NomPage" and contenuAction[3].text is not None):
                            if(comboLogiciel.get()=="Google Chrome"):
                                tabSite = contenuAction[3].text.split("- Google Chrome")
                            if(comboLogiciel.get()=="Internet Explorer"):
                                tabSite = contenuAction[3].text.split("- Internet Explorer")
                            if(comboLogiciel.get()=="Firefox"):
                                tabSite = contenuAction[3].text.split("- Mozilla Firefox")
                    #Ajout dans la liste de recherche si la page n'y est pas déjà
                    if(tabSite[0] not in listeRecherche):
                        listeRecherche.append(tabSite[0])
                #Affichage du nombre de pages visitées
                if(len(listeRecherche) > 1):
                    labelReponse['text'] = "L'étudiant a visité "+str(len(listeRecherche))+" pages"
                else:
                    labelReponse['text'] = "L'étudiant a visité "+str(len(listeRecherche))+" page"
        if(comboInfo1.get()=="Liste des"):
            if(comboInfo2.get()=="Pages visités"):
                tabInterro.heading("#0",text="Nom de la page")
                listeRecherche = []
                #Récupération d'un logiciel et de son contenu
                logicielChoisi = nomsLogiciel[comboLogiciel.current()]
                contenuLogiciel = logicielChoisi.getchildren()
                lesActions = contenuLogiciel[2].getchildren()
                for i in range(len(lesActions)-1):    
                    #Récupération du contenu de la i-ème action
                    contenuAction = lesActions[i].getchildren()
                    for i in range (len(contenuAction)):
                        #Récupération de la page visité
                        if (contenuAction[i].tag=="NomPage" and contenuAction[3].text is not None):
                            if(comboLogiciel.get()=="Google Chrome"):
                                tabSite = contenuAction[3].text.split("- Google Chrome")
                            if(comboLogiciel.get()=="Internet Explorer"):
                                tabSite = contenuAction[3].text.split("- Internet Explorer")
                            if(comboLogiciel.get()=="Firefox"):
                                tabSite = contenuAction[3].text.split("- Mozilla Firefox")
                    #Ajout dans la liste de recherche si la page n'y est pas déjà
                    if(tabSite[0] not in listeRecherche):
                        listeRecherche.append(tabSite[0])
                #Ajout des pages dans le tableau
                for page in listeRecherche:
                    tabInterro.insert("","end",None,text=page, values=())                                
        
#Création du label et de la liste déroulante concernant les logiciels
labelLogiciel = tk.Label(tabInterrogation,text="Logiciel :")
comboLogiciel = ttk.Combobox(tabInterrogation,state="readonly", values=listeLogiciel)

labelLogiciel.grid(sticky="W",row=0,column=0,padx=15,pady=5)
comboLogiciel.grid(sticky="W",row=0,column=1,pady=5)

#Création du label et de la liste déroulante concernant les informations
labelInfo = tk.Label(tabInterrogation,text="Types d'informations :")
comboInfo1 = ttk.Combobox(tabInterrogation,state="readonly", values=typeRecherche)
comboInfo1.configure(state="disabled")
comboInfo2 = ttk.Combobox(tabInterrogation,state="readonly")
comboInfo2.configure(state="disabled")
        

labelInfo.grid(sticky="W",row=0,column=2,padx=15,pady=5)
comboInfo1.grid(sticky="W",row=0,column=3,pady=5)
comboInfo2.grid(sticky="W",row=0,column=4,padx = 15,pady=5)

#Création du bouton de recherche
boutonRechercher = Button(tabInterrogation,text="Rechercher", command=rechercher)
boutonRechercher.grid(sticky="W",row=0,column=5,padx = 15,pady=5)

#Création du label contenant la réponse de la recherche
labelReponse = tk.Label(tabInterrogation,text="")
labelReponse.grid(sticky="W",row=1,column=0,columnspan=5,padx=15,pady=5)
       

def infomationsLogiciel(logiciel):
    #Récupérations des information du logiciel
    infoLogiciel = logiciel.getchildren()
    lesActions = infoLogiciel[2].getchildren()
    """
    Informations générales d'un logiciel
    """
    #Création d'une fenêtre annexe
    fenetreInformations = Toplevel()
    #paramétrage de la fenêtre
    fenetreInformations.geometry("700x300")
    fenetreInformations.title("Informations - " + logiciel.get('nom'))
    #Affichage des informations du logiciel
    lblNomLogiciel = tk.Label(fenetreInformations,text=logiciel.get('nom')).pack()
    lblHeureOuverture = tk.Label(fenetreInformations,text="Heure d'ouverture : " + infoLogiciel[0].text).pack()
    lblDureeOuvert = tk.Label(fenetreInformations,text="Temps d'utilisation : " + infoLogiciel[1].text).pack()
    tabOuverture = infoLogiciel[0].text.split(':')
    tabDuree = infoLogiciel[1].text.split(':')
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
    #Définition du tableau contenant les informations du logiciels
    tabActions = ttk.Treeview(fenetreInformations)
    tabActions["columns"]=("un","deux","trois","quatre")
    tabActions.column("#0",width=70,minwidth=50)
    tabActions.column("un",width=100,minwidth=100)
    tabActions.column("deux",width=100,minwidth=100)
    tabActions.column("trois",width=100,minwidth=100)
    tabActions.column("quatre",width=100,minwidth=100)

    #Définition des titre des colonnes du tableau
    tabActions.heading("#0",text="TypeAction",anchor=tk.W)
    tabActions.heading("un",text="Description",anchor=tk.W)
    tabActions.heading("deux",text="Heure",anchor=tk.W)
    tabActions.heading("trois",text="Nom de la page",anchor=tk.W)
    tabActions.heading("quatre",text="Saisie",anchor=tk.W)
    
    #remplissage du tableau
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

#fonction permettant de retirer les émoticones d'une chaîne de caractère pouvant être trouvé dans une saisie ou un nom de page
def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

#Définition des valeurs contenu dans la deuxième combobox concernant les informations
def choixInfo2(evt):
    remplirComboBox(evt)
    if comboInfo1.get()=="Liste des":
        comboInfo2['values'] = ["Pages visités"]

#Remplissage des listes déroulantes
def remplirComboBox(evt):
    #vérification qu'il y a eu une sélection
    if(comboLogiciel.current()!=-1):
        #Récupération des informations du logiciel choisi
        logicielChoisi = nomsLogiciel[comboLogiciel.current()]
        contenuLogiciel = logicielChoisi.getchildren()
        lesActions = contenuLogiciel[2].getchildren()
        typesAction = []
        #récupération des types d'actions ayant été effectuées
        for i in range(len(lesActions)):
            if lesActions[i].get('nom') not in typesAction:
                typesAction.append(lesActions[i].get('nom'))
        typeActionNav = []
        for i in range(len(typesAction)):
            typeActionNav.append(typesAction[i])
        typeActionNav.append("Pages visités")
        comboInfo2['values']=typesAction
        #Activation des liste déroulantes
        comboInfo1.configure(state="readonly")
        comboInfo2.configure(state="readonly")
        #Définition des actions possible pour les navigateurs de recherche
        if(comboLogiciel.get()in navigateurs):
            comboInfo1['values'] = typeRechercheNav
            comboInfo2['values'] = typeActionNav
        else:
            comboInfo1['values'] = typeRecherche
            comboInfo2['values'] = typesAction
    #Si rien n'est sélectionner désactiver les autres listes déroulantes
    if(comboLogiciel.current()==-1):
        comboInfo1.configure(state="disabled")
        comboInfo2.configure(state="disabled")


def onClick(evt):
    #Récupération de la ligne sur lequel le clic a été effectué
    if(tab_parent.index(tab_parent.select()) == 1 and evt.y >= 26):
        cy=evt.y-26
        index = int(cy/19)
        infomationsLogiciel(nomsLogiciel[index])

    
menu.bind("<Button 1>",onClick)
comboLogiciel.bind("<<ComboboxSelected>>",remplirComboBox)
comboInfo1.bind("<<ComboboxSelected>>",choixInfo2)
tab_parent.pack(expand=1,fill='both')
menu.mainloop()
