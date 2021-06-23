from datetime import date
from tkinter import messagebox

from gui.link_eingabe_fenster import createLinkEingabePage

#to do:
#-clean code: ergebnisseTabelleFenster
#- was ist bei internet problemen oder ausfall?

#2
#- Filter einbauen => ergebnisseTabelleFenster
#- Klick öffnet Fenster mit wichtigsten Infos? (Karte + Fotos?)
#- UI verbessern
#- Bemerkung nur was nicht alle haben?

aktuellesDatum = date.today()
alphaCloseDatum = date(2021,7,13)

if aktuellesDatum >= alphaCloseDatum:
    messagebox.showinfo(title="Testzeitraum abgeschlossen", message="Dein Testzeitraum für die Alpha-Version ist abgeschlossen.")
    exit()

createLinkEingabePage()
