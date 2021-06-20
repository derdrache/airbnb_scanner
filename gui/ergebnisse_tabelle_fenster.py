import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import html
import webbrowser

def ergebnissPage(df):
    global resultTable

    tableWindow = tk.Toplevel()
    tableWindow.title("Airbnb Ergebnisse")
    tableWindow.bind("<Motion>", callback)
    setStyle(tableWindow)

    resultTable = ResultTable(tableWindow, df)
    createTableExtraData(tableWindow, df)

def callback(event):
    global mousePosX, mousePosY
    mousePosX=event.x
    mousePosY= event.y

def setStyle(window):
    style = ThemedStyle(window)
    style.set_theme("clearlooks")
    style.configure("Treeview",
                    background="lightgrey",
                    fieldbackground="lightgrey")

class ResultTable:
    def __init__(self, root, df):

        self.sortierungsPrioList = []

        columnList = list(df.columns)
        self.table = ttk.Treeview(root, column=tuple(columnList))
        self.table["show"] = "headings"
        self.table.bind("<Double-1>", self.openRoomlinkInBrowser)

        self.fillTableHead(columnList)
        self.fillTableBody(df)

        self.table.pack(fill = "both" ,expand=True)

    def openRoomlinkInBrowser(self,event):
        selection = self.table.selection()
        urlLink = self.table.item(selection)['values'][9]

        webbrowser.open('{}'.format(urlLink))

    def fillTableHead(self,columns):
        for index, col in enumerate(columns):
            columnWidth = self.getTableColumnWidt(col)
            self.table.heading(col, text=col, anchor='w', command=lambda _col=col: PopupWindow(_col))
            self.table.column(col, anchor="w", width=columnWidth)

    def getTableColumnWidt(self,col):
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

    def fillTableBody(self,df):
        for index, row in df.iterrows():
            self.table.insert("",tk.END,text="", value =list(row))

class PopupWindow:
    def __init__(self, col):
        self.popupWindow  = tk.Tk()
        self.popupWindow.title(col)

        self.setStyle()

        popupFrame = ttk.Frame(self.popupWindow)

        buttonSortierungAZ = ttk.Button(popupFrame,
                                text= "Sort A-Z",
                                command= lambda: self.buttonTableSortColumn(col, False))
        buttonSortierungAZ.pack()

        buttonSortierungZA = ttk.Button(popupFrame,
                                text= "Sort Z-A",
                                command= lambda: self.buttonTableSortColumn(col, True))
        buttonSortierungZA.pack()

        buttonFilter = ttk.Button(popupFrame,
                                text= "Filter",
                                command= lambda: self.tabelFilterColumn(col))
        buttonFilter.pack()

        buttonReset = ttk.Button(popupFrame,
                                text= "reset",
                                command= lambda: self.buttonTableResetColumn(col))
        buttonReset.pack()


        popupFrame.pack()

    def setStyle(self):
        style = ThemedStyle(self.popupWindow)
        style.set_theme("clearlooks")

    def buttonTableSortColumn(self, col, reverse):

        self.sortPrio(col, reverse)
        self.tableHeaderChange()
        self.sortColumn()

        self.popupWindow.destroy()

    def sortPrio(self, col, reverse):

        if len(resultTable.sortierungsPrioList) == 0:
            resultTable.sortierungsPrioList.append([col , reverse, ""])
        else:
            for index, item in enumerate(resultTable.sortierungsPrioList):
                if item[0] == col:
                    resultTable.sortierungsPrioList[index][1] = reverse
                else:
                    resultTable.sortierungsPrioList.append([col , reverse, ""])

    def tableHeaderChange(self):
        for index, item in enumerate(resultTable.sortierungsPrioList):
            headerChange = item[0] + " " + str(index +1) + " " + self.getArrowForSort(item[1])
            resultTable.table.heading(item[0], text=headerChange)

    def getArrowForSort(self,reverse):
        pfeilHoch = html.unescape("&#x2191;")
        pfeilRunter = html.unescape("&#x2193;")

        if reverse:
            return pfeilHoch
        else:
            return pfeilRunter

    def sortColumn(self):
        rowIDArr = resultTable.table.get_children('')
        colDataArr = []

        #Daten von jeder Reihe mit den jeweiligen Spalten mit der ID speichern
        for rowID in rowIDArr:
            data = []
            for col in resultTable.sortierungsPrioList:
                tableData = resultTable.table.set(rowID, col[0]) #aus der Tabelle
                if tableData.isdigit():
                    tableData = int("".join([i for i in tableData if i.isdigit()]))#prüfen ob Zahlen
                if col[1] == True:
                    tableData = self.reversor(tableData) #für den Sort Key umgekehrte Reihnfolge
                data.append(tableData)

            data.append(rowID)
            colDataArr.append(data)
        #Datensortierung je nachdem wieviele Spalten zum Sortieren ausgewählt wurden
        colDataArr.sort(key=lambda data: tuple(data[:-1]))

        # re arrange items in sorted positions
        for index, value in enumerate(colDataArr):
            resultTable.table.move(value[-1], '', index)

    class reversor:
        def __init__(self, obj):
            self.obj = obj

        def __eq__(self, other):
            return other.obj == self.obj

        def __lt__(self, other):
            return other.obj < self.obj

    def tabelFilterColumn(self,col):
        print("in Arbeit")

    def buttonTableResetColumn(self,col):
        for item in resultTable.sortierungsPrioList:
            if item[0] == col:
                resultTable.table.heading(col, text=col)
                resultTable.sortierungsPrioList.remove(item)

        self.tableHeaderChange()
        self.sortColumn()

        self.popupWindow.destroy()

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
