import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import logic.airbnb_searcher as airbnb_searcher
import html


def windowErgebnisse(df):
    global table, sortierungsPrioArr
    tableWindow = tk.Toplevel()
    tableWindow.title("Airbnb Ergebnisse")
    tableWindow.bind("<Motion>", callback)

    tableWindow.grid_rowconfigure(0, weight=1)
    tableWindow.grid_columnconfigure(0, weight=1)

    roomCountText = tk.StringVar()
    roomDurchschnittpreisText = tk.StringVar()
    roomCountText.set(len(df.index))
    roomPreisSumme = 0

    tableWindowFrameA = tk.Frame(tableWindow)

    cols = list(df.columns)
    table = ttk.Treeview(tableWindowFrameA, column=tuple(cols))
    table["show"] = "headings"
    table.bind("<Double-1>", openTableLink)

    sortierungsPrioArr = []

    for index, col in enumerate(cols):
        columnWidth = getTableColumnWidt(col)
        table.heading(col, text=col, anchor='w', command=lambda _col=col: popupWindowTable(table, _col))
        table.column(col, anchor="w", width=columnWidth)

    #table.column("#0", anchor="w", width=1)

    for index, row in df.iterrows():
        table.insert("",tk.END,text="", value =list(row))
        roomPreisSumme += int(list(row)[3])

    roomDurchschnittpreisText.set(round(roomPreisSumme / len(df.index)))


    tableWindowFrameB = tk.Frame(tableWindow)

    label_a = tk.Label(master=tableWindowFrameB, text='Gefundene Unterkünfte:')
    labelAUpdate = tk.Label(master=tableWindowFrameB, textvariable=str(roomCountText))

    label_b = tk.Label(master=tableWindowFrameB, text='Durchschnittlicher Preis:')
    labelBUpdate = tk.Label(master=tableWindowFrameB, textvariable=roomDurchschnittpreisText)

    label_a.pack(side=tk.LEFT)
    labelAUpdate.pack(side=tk.LEFT)
    label_b.pack(side=tk.LEFT)
    labelBUpdate.pack(side=tk.LEFT)


    table.pack(expand=True, fill = "both")
    tableWindowFrameA.grid(sticky="nsew")
    tableWindowFrameB.grid()

def popupWindowTable(table, col):
    global mousePosX, mousePosY, popupWindow
    popupWindow  = tk.Tk()
    popupWindow.title(col)
    #popupWindow.geometry("+%d+%d" % (mousePosX, mousePosY))

    popupFrame = tk.Frame(popupWindow)

    buttonSortierungAZ = tk.Button(popupFrame,
                            width= buttonWidth,
                            height = buttonHeight,
                            text= "Sortierung A-Z",
                            command= lambda: buttonTableSortColumn(col, False))
    buttonSortierungZA = tk.Button(popupFrame,
                            width= buttonWidth,
                            height = buttonHeight,
                            text= "Sortierung Z-A",
                            command= lambda: buttonTableSortColumn(col, True))

    buttonFilter = tk.Button(popupFrame,
                            width= buttonWidth,
                            height = buttonHeight,
                            text= "Filter",
                            command= lambda: tabelFilterColumn(col))

    buttonReset = tk.Button(popupFrame,
                            width= buttonWidth,
                            height = buttonHeight,
                            text= "reset",
                            command= lambda: buttonTableResetColumn(col))

    buttonSortierungAZ.pack()
    buttonSortierungZA.pack()
    buttonFilter.pack()
    buttonReset.pack()

    popupFrame.pack()

def buttonTableSortColumn(col, reverse):

    sortPrio(col, reverse)
    tableHeaderChange()
    sortColumn()

    popupWindow.destroy()

def sortColumn():
    global sortierungsPrioArr
    rowIDArr = table.get_children('')
    colDataArr = []

    #Daten von jeder Reihe mit den jeweiligen Spalten mit der ID speichern
    for rowID in rowIDArr:
        data = []
        for col in sortierungsPrioArr:
            tableData = table.set(rowID, col[0]) #aus der Tabelle
            if tableData.isdigit():
                tableData = int("".join([i for i in tableData if i.isdigit()]))#prüfen ob Zahlen
            if col[1] == True:
                tableData = reversor(tableData) #für den Sort Key umgekehrte Reihnfolge
            data.append(tableData)

        data.append(rowID)
        colDataArr.append(data)
    #Datensortierung je nachdem wieviele Spalten zum Sortieren ausgewählt wurden
    colDataArr.sort(key=lambda data: tuple(data[:-1]))

    # re arrange items in sorted positions
    for index, value in enumerate(colDataArr):
        table.move(value[-1], '', index)

class reversor:
    def __init__(self, obj):
        self.obj = obj

    def __eq__(self, other):
        return other.obj == self.obj

    def __lt__(self, other):
        return other.obj < self.obj

def getArrowForSort(reverse):
    pfeilHoch = html.unescape("&#x2191;")
    pfeilRunter = html.unescape("&#x2193;")

    if reverse:
        return pfeilHoch
    else:
        return pfeilRunter

def tabelFilterColumn(col):
    print("in Arbeit")

def buttonTableResetColumn(col):
    for item in sortierungsPrioArr:
        if item[0] == col:
            table.heading(col, text=col)
            sortierungsPrioArr.remove(item)

    tableHeaderChange()
    sortColumn()

    popupWindow.destroy()

def getTableColumnWidt(col):
    if col == "Titel"or col== "Bewertung":
        return 220
    elif col == "Art":
        return 100
    elif col == "Extras":
        return 150
    elif col == "Gäste" or col == "Bemerkung" :
        return 70
    elif col == "Link":
        return 170
    else:
        return 50

def openTableLink(selection):
    selectionID = table.selection()
    inputItem = table.item(selectionID)['values'][9]#Links

    import webbrowser
    webbrowser.open('{}'.format(inputItem))

def callback(event):
    global mousePosX, mousePosY
    mousePosX=event.x
    mousePosY= event.y

def sortPrio(col, reverse):
    if len(sortierungsPrioArr) == 0:
        sortierungsPrioArr.append([col , reverse, ""])
    else:
        for index, item in enumerate(sortierungsPrioArr):
            if item[0] == col:
                sortierungsPrioArr[index][1] = reverse
            else:
                sortierungsPrioArr.append([col , reverse, ""])

def tableHeaderChange():
    for index, item in enumerate(sortierungsPrioArr):
        headerChange = item[0] + " " + str(index +1) + " " + getArrowForSort(item[1])
        table.heading(item[0], text=headerChange)

#windowLinkEingabe()
