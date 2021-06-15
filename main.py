from datetime import date
from tkinter import messagebox

from gui.link_eingabe_fenster import linkEingabePage

#to do:
#- df leer => message

#2
#- Klick öffnet Fenster mit wichtigsten Infos? (Karte + Fotos?)
#- Code verbessern
#- UI verbessern
#- Bemerkung nur was nicht alle haben?

aktuellesDatum = date.today()
alphaCloseDatum = date(2021,6,13)

if aktuellesDatum == alphaCloseDatum:
    messagebox.showinfo(title="Testzeitraum abgeschlossen", message="Dein Testzeitraum für die Alpha-Version ist abgeschlossen.")
    exit()

linkEingabePage()
