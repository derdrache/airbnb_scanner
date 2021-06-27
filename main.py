from datetime import date
from tkinter import messagebox

from gui.link_eingabe_fenster import createLinkEingabePage

#to do:
#- UI verbessern

#2
#- calculateRabatt wirft manchmal ein Fehler => priceOld == 0??
#- Filter einbauen => ergebnisseTabelleFenster
#- Klick öffnet Fenster mit wichtigsten Infos? (Karte + Fotos?)

#- Bemerkung nur was nicht alle haben?


def startApp():
    licenseBool = checkEasylicenseStatus()

    if not licenseBool:
        showMessageAndCloseApp()
    createLinkEingabePage()

def checkEasylicenseStatus():
    aktuellesDatum = date.today()
    alphaCloseDatum = date(2021,7,13)

    if aktuellesDatum >= alphaCloseDatum:
        return False
    else:
        return True

def showMessageAndCloseApp():
    messagebox.showinfo(title="Testzeitraum abgeschlossen", message="Dein Testzeitraum für die Alpha-Version ist abgeschlossen.")
    exit()


startApp()
