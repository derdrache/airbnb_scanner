from datetime import date
from tkinter import messagebox

from gui.link_eingabe_fenster import createLinkEingabePage

#to do:
#- UI verbessern
#- Bemerkung nur was nicht alle haben?
#- Filter einbauen => ergebnisseTabelleFenster
#- calculateRabatt wirft manchmal ein Fehler => priceOld == 0??

#2
#- Klick öffnet Fenster mit wichtigsten Infos? (Karte + Fotos?)




def startApp():
    licenseBool = checkEasylicenseStatus()

    if not licenseBool:
        showMessageAndCloseApp()
    createLinkEingabePage()

def checkEasylicenseStatus():
    aktuellesDatum = date.today()
    alphaCloseDatum = date(2021,10,1)

    if aktuellesDatum >= alphaCloseDatum:
        return False
    else:
        return True

def showMessageAndCloseApp():
    messagebox.showinfo(title="Testzeitraum abgeschlossen", message="Dein Testzeitraum ist abgeschlossen.")
    exit()


startApp()
