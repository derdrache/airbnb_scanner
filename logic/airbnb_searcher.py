from bs4 import BeautifulSoup
import pandas as pd # All database operations
import requests     # HTTP requests


def searchAirbnb(urlArr):
	rooms = getAllRooms(urlArr)

	return getDataframeFromRoomData(rooms)

def getAllRooms(urlArr):
    allRooms = []
    for url in urlArr:
        if url == "":
            break
        pages = getAllPagesAsList(url)
        rooms = getRoomFromAllPages(pages)

        allRooms = allRooms + rooms

    return allRooms

def getAllPagesAsList(url):
	result = []

	while url != "no next page":
		page = getPageAsSoup(url)
		result = result + [page]
		url = findNextPage(page)

	return result
def getPageAsSoup(url):
	result = requests.get(url)
	content = result.content

	return BeautifulSoup(content, features = "lxml")
def findNextPage(soupPage):
	try:
		nextpage = "https://airbnb.de" + soupPage.find("a", {"class":"_za9j7e"})["href"]
	except: # When he can't find the button, I assume he reached the end
		nextpage = "no next page"

	return nextpage

def getRoomFromAllPages(soupPages):
	result = []

	for page in soupPages:
		rooms = getRoomsFromOnePage(page)
		for room in rooms:
			result.append(room)

	return result
def getRoomsFromOnePage(soupPage):
	rooms = soupPage.findAll("div", {"class": "_8ssblpx"})
	result = []

	for room in rooms:
		result.append(room)

	return result

def getDataframeFromRoomData(rooms):
	roomData = []
	lables = ["Titel", "Art", "Bewertung","Preis", "Preis vorher", "Rabatt", "Bemerkung", "Extras", "Gäste", "Link"]

	for room in rooms:
		price= getRoomPrice(room)
		priceBefore = getRoomOldPrice(room)

		arr = [getRoomName(room), getTypeOfRoom(room), getRoomRating(room), price,
		       priceBefore ,calculateRabatt(price, priceBefore), getRoomComment(room),getRoomExtras(room), getRoomPersonNumber(room), getRoomLink(room)]
		roomData.append(arr)

	roomData = deleteDuplicatRooms(roomData)
	df = pd.DataFrame(roomData, columns=lables)

	return df
def getRoomName(listing):
	return listing.find("meta")["content"]
def getTypeOfRoom(listing):
	text = listing.find("div", {"class": "_1tanv1h"}).text

	return text.split(" ")[0] + " " +  text.split(" ")[1]
def getRoomLink(listing):
	return "http://airbnb.de" + listing.find("a")["href"]
def getRoomPrice(listing):
	try:
		priceText = listing.find("span", {"class": "_155sga30"}).text
		priceText = priceText.split("€")[0]
		priceText = priceText.replace(".", "")
	except:
		priceText = "0"

	return priceText
def getRoomOldPrice(listing):
	try:
		priceText = listing.find("span", {"class": "_16shi2n"}).text
		priceText = priceText.split("€")[0]
		priceText = priceText.replace(".", "")
	except:
		priceText = ""

	return priceText
def calculateRabatt(price, priceBefore):
	if priceBefore == "":
		priceBefore = price

	return round(100 - (int(price) / int(priceBefore) *100))
def getRoomRating(listing):
	try:
		return listing.find("div", {"class": "_1hxyyw3"}).text
	except:
		return ""
def getRoomComment(listing):
	try:
		bemerkung = listing.find("div", {"class": "_gxjeqd"}).text
		if "Sehr" in bemerkung:
			bemerkung = bemerkung.split("·")[0]
		return bemerkung
	except:
		return ""
def getRoomExtras(listing):
	result = ""
	extras = listing.find_all("div", {"class": "_3c0zz1"})

	if len(extras)>1:
		extras = extras[1].text
		extrasArr = extras.split("·")

		for extra in extrasArr:
			if not "WLAN" in extra and not "Küche" in extra:
				result += extra + "·"
		return result

	return ""
def getRoomPersonNumber(listing):
	return listing.find("div", {"class": "_3c0zz1"}).text.split("·")[0]

def deleteDuplicatRooms(roomsArr):
	newRoomsArr = []

	for room in roomsArr:
		newCheck = True
		for newRoom in newRoomsArr:
			if newRoom[0] == room[0]:
				newCheck = False

		if newCheck:
			newRoomsArr.append(room)

	return newRoomsArr
