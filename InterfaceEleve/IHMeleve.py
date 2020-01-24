from tkinter import *
import tkinter.font as tkFont
import tkinter.scrolledtext as tkst
     
    

fenetreCommencerExercice = Tk()
fenetreCommencerExercice.geometry('200x50')
fenetreCommencerExercice.title("Système d'analyse de traces - Commencer l'exercice")

def fenetreEnSavoirPlus(self):
    fenetreESP = Tk()
    fenetreESP.attributes("-topmost",True)
    fenetreESP.title("En savoir plus")
    editArea = tkst.ScrolledText(master = fenetreESP, wrap = WORD)
    editArea.pack(padx=10,pady=10,fill=BOTH,expand=True)
    editArea.insert(INSERT,
                    """\
POLITIQUE DE PROTECTION DES DONNÉES PERSONNELLES
Dernière mise à jour : 03/12/2019
                    
    L’IUT de Bayonne et du Pays Basque est soucieux de la protection des données personnelles. Il met en œuvre une démarche d'amélioration continue de sa conformité au Règlement général de protection des données (RGPD), à la Directive ePrivacy, ainsi qu'à la loi n° 78-17 du 6 janvier 1978 dite Informatique et Libertés pour assurer le meilleur niveau de protection à vos données personnelles.\nPour toute information sur la protection des données personnelles, vous pouvez également consulter le site de la Commission Nationale de l'Informatique et des Libertés www.cnil.fr.\n\nQui est le responsable du traitement de mes données personnelles ?
                    
    Le responsable de traitement est la société qui définit pour quel usage et comment vos données personnelles sont utilisées.
Les données personnelles collectées sur l’application d’analyse de traces sont traitées par :\nIUT de Bayonne et du Pays Basque
Domiciliées: 2 Allée du Parc Montaury, 64600 Anglet
Ci-après nommé : IUT


Pourquoi l’IUT collecte mes données personnelles ?

L’IUT utilise vos données personnelles principalement pour les finalités suivantes :
    La pédagogie : Nous avons besoin des informations qui vous concerne pour améliorer l’évaluation vous concernant lors de votre parcours au sein de l’IUT informatique.
    

Quelles sont les données personnelles qui sont collectées me concernant ?

Quelles données ?

    Nous collectons et traitons notamment vos clics, sites consultés, application, mouvements de souris, textes saisis. Dans certains cas, nous pouvons collecter des données de .
Toutes ces données sont collectées automatiquement du fait de vos actions sur l’application.

Quand ?

Nous collectons les informations que vous nous fournissez quand :
    vous commencez un exercice, et après avoir recueilli votre consentement.
    
Quelles sont les communications que je suis susceptible de recevoir ?

Les informations
Statistiques : Suite à un exercice ou d’un contrôle, vous pourriez recevoir un email afin de vous annoncez les statistiques générales dudit exercice ou contrôle; ou bien lors d’un cours en amphithéâtre où le professeur vous fera le retour.
                    """)
    boutonFermer= Button(fenetreESP,text="Fermer", command=fenetreESP.destroy)
    boutonFermer.pack(side=RIGHT)
    fenetreESP.pack()

def command():
    fenetreAutorisation = Tk()
    fenetreAutorisation.title("New Window")
    label = Label(fenetreAutorisation, text="Acceptez-vous que vos données soient enregistrées dans un cadre pédagogique ?")
    label.pack()
    
    labelEnSavoirPlus = Label(fenetreAutorisation, text="En savoir plus",fg="blue")
    labelEnSavoirPlus.pack(side = LEFT)
    myfont = tkFont.Font(labelEnSavoirPlus, labelEnSavoirPlus.cget("font"))
    myfont.configure(underline = True)
    labelEnSavoirPlus.configure(font=myfont)
    labelEnSavoirPlus.bind("<Button-1>", fenetreEnSavoirPlus)

    boutonAccepter = Button(fenetreAutorisation,text="J'accepte", command=fenetreAutorisation.destroy)
    boutonAccepter.pack(side=RIGHT)
    boutonRefuser= Button(fenetreAutorisation,text="Je refuse", command=fenetreAutorisation.destroy)
    boutonRefuser.pack(side=RIGHT)

    fenetreAutorisation.mainloop()
     
newwindow = Button(fenetreCommencerExercice, text="Commencer exercice", command=command)
newwindow.pack()
fenetreCommencerExercice.mainloop()
