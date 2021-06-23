import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedStyle
import html
import webbrowser

def createErgebnissPage(df):
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
        self.df = df

        self.columnList = list(df.columns)
        self.table = ttk.Treeview(root, column=tuple(self.columnList))
        self.table["show"] = "headings"
        self.table.bind("<Double-1>", self.openRoomlinkInBrowser)

        self.fillTableHead()
        self.fillTableBody()

        self.table.pack(fill = "both" ,expand=True)

    def openRoomlinkInBrowser(self,event):
        selection = self.table.selection()
        urlLink = self.table.item(selection)['values'][9]

        webbrowser.open('{}'.format(urlLink))

    def fillTableHead(self):
        for index, col in enumerate(self.columnList):
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

    def fillTableBody(self):
        for index, row in self.df.iterrows():
            self.table.insert("",tk.END,text="", value =list(row))

    def changeSort(self, sortPrioRowIDList):
        for index, value in enumerate(sortPrioRowIDList):
            resultTable.table.move(value[-1], '', index)

class PopupWindow:
    def __init__(self, col):
        self.col = col

        self.popupWindow  = tk.Tk()
        self.popupWindow.title(self.col)

        self.setStyle()

        self.layout()

    def setStyle(self):
        style = ThemedStyle(self.popupWindow)
        style.set_theme("clearlooks")

    def layout(self):
        popupFrame = ttk.Frame(self.popupWindow)

        buttonSortierungAZ = ttk.Button(popupFrame,
                                text= "Sort A-Z",
                                command= lambda: self.sortTable(self.col, False))
        buttonSortierungAZ.pack()

        buttonSortierungZA = ttk.Button(popupFrame,
                                text= "Sort Z-A",
                                command= lambda: self.sortTable(self.col, True))
        buttonSortierungZA.pack()

        buttonFilter = ttk.Button(popupFrame,
                                text= "Filter",
                                command= lambda: self.tabelFilterColumn(self.col))
        buttonFilter.pack()

        buttonReset = ttk.Button(popupFrame,
                                text= "reset",
                                command= lambda: self.sortFilterReset(self.col))
        buttonReset.pack()


        popupFrame.pack()

    def sortTable(self, col, reverse):

        self.changeTableSortPrioList(col, reverse)
        self.changeTableHeader()
        self.sortColumn()

        self.popupWindow.destroy()

    def changeTableSortPrioList(self, col, reverse):

        if len(resultTable.sortierungsPrioList) == 0:
            resultTable.sortierungsPrioList.append([col , reverse])
        else:
            for index, item in enumerate(resultTable.sortierungsPrioList):
                if item[0] == col:
                    resultTable.sortierungsPrioList[index][1] = reverse
                else:
                    resultTable.sortierungsPrioList.append([col , reverse])

    def changeTableHeader(self):
        for index, item in enumerate(resultTable.sortierungsPrioList):
            headerChange = item[0] + " " + str(index +1) + " " + self.getSortArrow(item[1])
            resultTable.table.heading(item[0], text=headerChange)

    def getSortArrow(self,reverse):
        pfeilHoch = html.unescape("&#x2191;")
        pfeilRunter = html.unescape("&#x2193;")

        if reverse:
            return pfeilHoch
        else:
            return pfeilRunter
    #sortColumn clean code
    def sortColumn(self):
        sortPrioRowIDList = self.combineSortprioRowID()

        sortPrioRowIDList.sort(key=lambda data: tuple(data[:-1]))

        resultTable.changeSort(sortPrioRowIDList)

    def combineSortprioRowID(self):
        tableRowList = resultTable.table.get_children('')
        combinedList = []

        for rowID in tableRowList:
            columnTableData = resultTable.table.set(rowID, sortPrio[0])
            sortPrioRowID = []

            for sortPrio in resultTable.sortierungsPrioList:
                if sortPrio[1] == True:
                    columnTableData = self.reversor(columnTableData) #für den Sort Key umgekehrte Reihnfolge


            sortPrioRowID.append(columnTableData)
            sortPrioRowID.append(rowID)

            combinedList.append(sortPrioRowID)

        return combinedList

    class reversor:
        def __init__(self, obj):
            self.obj = obj

        def __eq__(self, other):
            return other.obj == self.obj

        def __lt__(self, other):
            return other.obj < self.obj

    def sortColumnTest(self, col):
        l = [(resultTable.table.set(k, col), k) for k in resultTable.table.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            resultTable.table.move(k, '', index)
        # reverse sort next time
        #tv.heading(col, command=lambda: \
        #           treeview_sort_column(tv, col, not reverse))

    #reversor clean code


    def tabelFilterColumn(self,col):
        print("in Arbeit")

    def sortFilterReset(self,col):
        for item in resultTable.sortierungsPrioList:
            if item[0] == col:
                resultTable.table.heading(col, text=col)
                resultTable.sortierungsPrioList.remove(item)

        self.changeTableHeader()
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
