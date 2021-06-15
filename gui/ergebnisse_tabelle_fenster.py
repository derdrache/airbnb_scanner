import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import html


def ergebnissPage(df):
    global sortierungsPrioList

    sortierungsPrioList = []

    tableWindow = tk.Toplevel()
    tableWindow.title("Airbnb Ergebnisse")
    tableWindow.bind("<Motion>", callback)

    setStyle(tableWindow)
    expandFullWindowSize(tableWindow)


    createTable(tableWindow, df)
    createTableExtraData(tableWindow, df)

def callback(event):
    global mousePosX, mousePosY
    mousePosX=event.x
    mousePosY= event.y

def setStyle(window):
    style = ThemedStyle(window)
    style.set_theme("clearlooks")

def expandFullWindowSize(window):
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)


def createTable(window, df):
    global table

    frame = ttk.Frame(window)

    columnsList = list(df.columns)
    table = ttk.Treeview(window, column=tuple(columnsList))
    table["show"] = "headings"
    table.bind("<Double-1>", openTableLink)

    fillTableHead(columnsList)
    fillTableBody(df)

    table.pack(expand=True, fill = "both")

    frame.pack()

def openTableLink(selection):
    selectionID = table.selection()
    inputItem = table.item(selectionID)['values'][9]#Links

    import webbrowser
    webbrowser.open('{}'.format(inputItem))

def fillTableHead(cols):
    for index, col in enumerate(cols):
        columnWidth = getTableColumnWidt(col)
        table.heading(col, text=col, anchor='w', command=lambda _col=col: popupWindowTable(table, _col))
        table.column(col, anchor="w", width=columnWidth)

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

def popupWindowTable(table, col):
    global mousePosX, mousePosY, popupWindow
    popupWindow  = tk.Tk()
    popupWindow.title(col)

    setStyle(popupWindow)

    popupFrame = ttk.Frame(popupWindow)

    buttonSortierungAZ = ttk.Button(popupFrame,
                            text= "Sort A-Z",
                            command= lambda: buttonTableSortColumn(col, False))
    buttonSortierungAZ.pack()

    buttonSortierungZA = ttk.Button(popupFrame,
                            text= "Sort Z-A",
                            command= lambda: buttonTableSortColumn(col, True))
    buttonSortierungZA.pack()

    buttonFilter = ttk.Button(popupFrame,
                            text= "Filter",
                            command= lambda: tabelFilterColumn(col))
    buttonFilter.pack()

    buttonReset = ttk.Button(popupFrame,
                            text= "reset",
                            command= lambda: buttonTableResetColumn(col))
    buttonReset.pack()


    popupFrame.pack()

def fillTableBody(df):
    for index, row in df.iterrows():
        table.insert("",tk.END,text="", value =list(row))

def buttonTableSortColumn(col, reverse):

    sortPrio(col, reverse)
    tableHeaderChange()
    sortColumn()

    popupWindow.destroy()

def sortPrio(col, reverse):
    if len(sortierungsPrioList) == 0:
        sortierungsPrioList.append([col , reverse, ""])
    else:
        for index, item in enumerate(sortierungsPrioList):
            if item[0] == col:
                sortierungsPrioList[index][1] = reverse
            else:
                sortierungsPrioList.append([col , reverse, ""])

def tableHeaderChange():
    for index, item in enumerate(sortierungsPrioList):
        headerChange = item[0] + " " + str(index +1) + " " + getArrowForSort(item[1])
        table.heading(item[0], text=headerChange)

def getArrowForSort(reverse):
    pfeilHoch = html.unescape("&#x2191;")
    pfeilRunter = html.unescape("&#x2193;")

    if reverse:
        return pfeilHoch
    else:
        return pfeilRunter

def sortColumn():
    rowIDArr = table.get_children('')
    colDataArr = []

    #Daten von jeder Reihe mit den jeweiligen Spalten mit der ID speichern
    for rowID in rowIDArr:
        data = []
        for col in sortierungsPrioList:
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

def tabelFilterColumn(col):
    print("in Arbeit")

def buttonTableResetColumn(col):
    for item in sortierungsPrioList:
        if item[0] == col:
            table.heading(col, text=col)
            sortierungsPrioList.remove(item)

    tableHeaderChange()
    sortColumn()

    popupWindow.destroy()


def createTableExtraData(window, df):
    tableWindowFrameB = ttk.Frame(window)

    label_a = tk.Label(master=tableWindowFrameB, text='Gefundene Unterkünfte:')
    label_a.pack(side=tk.LEFT)

    roomNumberText = tk.StringVar(window, len(df.index))
    labelAUpdate = tk.Label(master=tableWindowFrameB, textvariable=str(roomNumberText))
    labelAUpdate.pack(side=tk.LEFT)

    label_b = tk.Label(master=tableWindowFrameB, text='Durchschnittlicher Preis:')
    label_b.pack(side=tk.LEFT)

    roomPreisSumme = getRoomPreisSumme(df)
    roomDurchschnittpreis = round(roomPreisSumme / len(df.index))
    roomDurchschnittpreisText = tk.StringVar(window, roomDurchschnittpreis)
    labelBUpdate = tk.Label(master=tableWindowFrameB, textvariable=roomDurchschnittpreisText)
    labelBUpdate.pack(side=tk.LEFT)

    tableWindowFrameB.pack()

def getRoomPreisSumme(df):
    summe= 0
    for index, row in df.iterrows():
        summe += int(list(row)[3])
    return summe
