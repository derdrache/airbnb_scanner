from bs4 import BeautifulSoup
import pandas as pd
import requests


class Room:
	def __init__(self, roomListing):
		self.listing = roomListing

	def getRoomName(self):
		try:
			return self.listing.find("meta")["content"]
		except:
			return ""

	def getTypeOfRoom(self):
		text = self.listing.find("div", {"class": "_1tanv1h"}).text

		return text.split(" ")[0] + " " +  text.split(" ")[1]

	def getRoomLink(self):
		return "http://airbnb.de" + self.listing.find("a")["href"]

	def getRoomPrice(self):
		try:
			priceText = self.listing.find("span", {"class": "_155sga30"}).text
			priceText = priceText.split("€")[0]
			priceText = priceText.replace(".", "")
		except:
			priceText = "0"

		return priceText

	def getRoomOldPrice(self):
		try:
			priceText = self.listing.find("span", {"class": "_16shi2n"}).text
			priceText = priceText.split("€")[0]
			priceText = priceText.replace(".", "")
		except:
			priceText = ""

		return priceText

	def calculateRabatt(self):
		price = self.getRoomPrice()
		priceOld = self.getRoomOldPrice()

		if priceOld == "":
			priceOld = price

		return round(100 - (int(price) / int(priceOld) *100))

	def getRoomRating(self):
		try:
			return self.listing.find("div", {"class": "_1hxyyw3"}).text
		except:
			return ""

	def getRoomComment(self):
		try:
			bemerkung = self.listing.find("div", {"class": "_gxjeqd"}).text
			if "Sehr" in bemerkung:
				bemerkung = bemerkung.split("·")[0]
			return bemerkung
		except:
			return ""

	def getRoomExtras(self):
		result = ""
		extras = self.listing.find_all("div", {"class": "_3c0zz1"})

		if len(extras)>1:
			extras = extras[1].text
			extrasArr = extras.split("·")

			for extra in extrasArr:
				if not "WLAN" in extra and not "Küche" in extra:
					result += extra + "·"
			return result

		return ""

	def getRoomPersonNumber(self):
		return self.listing.find("div", {"class": "_3c0zz1"}).text.split("·")[0]

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
	try:
		request = requests.get(url)
		content = request.content

		return BeautifulSoup(content, features = "lxml")
	except requests.ConnectionError:
		return None

def findNextPage(soupPage):
	try:
		nextpage = "https://airbnb.de" + soupPage.find("a", {"class":"_za9j7e"})["href"]
	except: # When he can't find the button, I assume he reached the end
		nextpage = "no next page"

	return nextpage

def getRoomFromAllPages(soupPages):
	result = []

	for page in soupPages:
		if page != None:
			rooms = getRoomsFromOnePage(page)
			for room in rooms:
				result.append(room)

	return result
def getRoomsFromOnePage(soupPage):
	listings = soupPage.findAll("div", {"class": "_8ssblpx"})
	roomList = []

	for listing in listings:
		roomList.append(Room(listing))

	return roomList

def getDataframeFromRoomData(rooms):
	roomData = []
	lables = ["Titel", "Art", "Bewertung","Preis", "Preis vorher", "Rabatt", "Bemerkung", "Extras", "Gäste", "Link"]

	for room in rooms:
		if room.getRoomName() != "":
			arr = [room.getRoomName(), room.getTypeOfRoom(), room.getRoomRating(),
				   room.getRoomPrice(),room.getRoomOldPrice() ,room.calculateRabatt(),
				   room.getRoomComment(),room.getRoomExtras(), room.getRoomPersonNumber(),
				   room.getRoomLink()]

			roomData.append(arr)

	roomData = deleteDuplicatRooms(roomData)
	df = pd.DataFrame(roomData, columns=lables)

	return df

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
