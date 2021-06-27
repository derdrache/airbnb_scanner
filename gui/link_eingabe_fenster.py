import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle

import logic.airbnb_searcher as airbnb_searcher
import gui.ergebnisse_tabelle_fenster as ergebnisseTabelleFenster

font = "helevetica"
fontSize = 18
paddings = {'padx': 5, 'pady': 5}

def createLinkEingabePage():
    global eingabeWindow

    eingabeWindow = tk.Tk()
    eingabeWindow.title("Airbnb suche")
    eingabeWindow.bind('<Return>', enterKey)
    setStyle(eingabeWindow)

    pageFrame = ttk.Frame(eingabeWindow, highlightbackground="green", highlightcolor="green", highlightthickness=1)

    createLinkCountText(pageFrame)
    createLinkListBox(pageFrame)
    createLinkInput(pageFrame)
    createSearchStart(pageFrame)

    pageFrame.pack(pady = 20)

    eingabeWindow.mainloop()

def createErrorMessage(text):
    messagebox.showinfo(title="Link Error", message=text)

def enterKey(event):
    if enterLinkInput.get() != "":
        functionButtonAddLink()

def setStyle(window):
    backgroundColor = "#856ff8"
    window.configure(bg=backgroundColor)

    style = ThemedStyle(window)
    style.set_theme("clearlooks")

    style.configure('TFrame', background=backgroundColor)
    style.configure('TLabel', background=backgroundColor, font=(font, fontSize))
    style.configure('TButton', background=backgroundColor,font=(font, fontSize))
    style.map('TButton', background=[('active',backgroundColor)])

def createLinkCountText(window):
    global countLinkText
    frame = ttk.Frame(window)
    label = ttk.Label(master=frame, text='Eingefügte Links: ')
    countLinkText = tk.StringVar()
    labelUpdate = ttk.Label(master=frame, textvariable=countLinkText)

    label.pack(side=tk.LEFT)
    labelUpdate.pack(side=tk.LEFT)
    frame.pack(pady = 10)

def createLinkListBox(window):
    global linkBox

    frame = ttk.Frame(window)
    linkBox = tk.Listbox(master=frame, selectmode='browse', width=110, height = 6)
    linkBox.pack()
    frame.pack(pady = 10)

def createLinkInput(window):
    global enterLinkInput

    frame = ttk.Frame(window)
    enterLinkLabel = ttk.Label(master=frame, text="Hier den Link einfügen: ")
    enterLinkInput = ttk.Entry(master=frame,font=(font, fontSize))
    buttonLinkAdd = ttk.Button(master=frame,text= "+", command=functionButtonAddLink)
    buttonLinkDelete = ttk.Button(master = frame,text= "-", command=functionButtonLinkDelete)

    enterLinkLabel.pack(side=tk.LEFT)
    enterLinkInput.pack(side=tk.LEFT, padx = 10)
    buttonLinkAdd.pack(side=tk.LEFT, padx = 10)
    buttonLinkDelete.pack(side=tk.LEFT)
    frame.pack(pady = 10)

def functionButtonAddLink():
    newLink = enterLinkInput.get()
    enterLinkInput.delete(0,tk.END)

    if checkLink(newLink):
        linkBox.insert("end", newLink)
    else:
        createErrorMessage("Der eingegebene Link entspricht nicht den Vorgaben")

    updateCountLinkText()

def checkLink(link):
    airbnbSignatur = "https://www.airbnb"
    airbnbSuchzeichen = "/s/"

    return link != "" and airbnbSignatur in link and airbnbSuchzeichen in link

def functionButtonLinkDelete():
    deleteLink()
    updateCountLinkText()

def deleteLink():
    auswahlIndex = linkBox.curselection()[0]
    linkBox.delete(auswahlIndex)

def updateCountLinkText():
    number = len(linkBox.get(0,tk.END))
    countLinkText.set(number)

    eingabeWindow.update()

def createSearchStart(window):
    frame = ttk.Frame(window)
    buttonStart = ttk.Button(master=frame ,text = "Suchen", command= buttonStartFunction)
    buttonStart.pack()
    frame.pack(pady = 10)

def buttonStartFunction():
    startSearch()
    resetEingabe()

def startSearch():
    linkList = linkBox.get(0,tk.END)
    searchResults = airbnb_searcher.searchAirbnb(linkList)
    if not searchResults.empty:
        ergebnisseTabelleFenster.createErgebnissPage(searchResults)
    else:
        createErrorMessage("Die Suche hat keine Ergebnisse gefunden. Bitte versuch es mit einem anderen Link oder prüfe deine Internetverbindung")

def resetEingabe():
    countLinkText.set("")
    linkBox.delete(0, tk.END)
