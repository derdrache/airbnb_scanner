from bs4 import BeautifulSoup
from selenium import webdriver
# The following packages will also be used in this tutorial
import pandas as pd # All database operations
import numpy as np  # Numerical operations
import time         # Tracking time
import requests     # HTTP requests
import re           # String manipulation
from sklearn.feature_extraction.text import CountVectorizer # BagOfWords (cleaning)
from joblib import Parallel, delayed # Parallellization of tasks


def deleteChar(str):
	newStr = ""

	for char in str:
		if char != ".":
			newStr += char

	return newStr



def getPage(url):
	''' returns a soup object that contains all the information
	of a certain webpage'''
	result = requests.get(url)
	content = result.content
	return BeautifulSoup(content, features = "lxml")

def findNextPage(soupPage):
	''' Finds the next page with listings if it exists '''
	try:
		nextpage = "https://airbnb.de" + soupPage.find("a", {"class":"_za9j7e"})["href"]
	except: # When he can't find the button, I assume he reached the end
		nextpage = "no next page"

	return nextpage

def getPages(url):
	''' This function returns all the links to the pages containing
	listings for one particular city '''
	result = []
	while url != "no next page":
		page = getPage(url)
		result = result + [page]
		url = findNextPage(page)
	return result

def getRoomClasses(soupPage):
	''' This function returns all the listings that can
	be found on the page in a list.'''
	rooms = soupPage.findAll("div", {"class": "_8ssblpx"})
	result = []
	for room in rooms:
		result.append(room)
	return result

def getAllRoomClasses(soupPages):
	result = []
	for page in soupPages:
		rooms = getRoomClasses(page)
		for room in rooms:
			result.append(room)
	return result

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

def listingRoomDatatoTable(rooms):
	roomData = []
	lables = ["Titel", "Art", "Bewertung","Preis", "Preis vorher", "Rabatt", "Bemerkung", "Extras", "Gäste", "Link"]

	for room in rooms:
		price= getListingPrice(room)
		priceBefore = getListingPriceBefore(room)

		arr = [getListingTitle(room), getTopRowWohungsart(room), getListingRating(room), price,
		       priceBefore ,calculateRabatt(price, priceBefore), getListingBemerkung(room),getListingExtra(room), getPersonenAnzahl(room), getListingLink(room)]
		roomData.append(arr)

	roomData = deleteDuplicatRooms(roomData)
	#df = pd.DataFrame.from_records(roomData, columns=lables)
	df = pd.DataFrame(roomData, columns=lables)
	return df

def getListingTitle(listing):
	''' This function returns the title of the listing'''
	return listing.find("meta")["content"]

def getTopRowWohungsart(listing):
	''' Returns the top row of listing information'''
	text = listing.find("div", {"class": "_1tanv1h"}).text

	return text.split(" ")[0] + " " +  text.split(" ")[1]

def getListingLink(listing):
	''' This function returns the link of the listing'''
	return "http://airbnb.de" + listing.find("a")["href"]

def getListingPrice(listing):
	try:
		priceText = listing.find("span", {"class": "_155sga30"}).text
		priceText = priceText.split("€")[0]
		priceText = deleteChar(priceText)
	except:
		priceText = "0"

	return priceText

def getListingPriceBefore(listing):
	try:
		priceText = listing.find("span", {"class": "_16shi2n"}).text
		priceText = priceText.split("€")[0]
		priceText = deleteChar(priceText)
	except:
		priceText = ""

	return priceText

def calculateRabatt(price, priceBefore):
	if priceBefore == "":
		priceBefore = price

	return round(100 - (int(price) / int(priceBefore) *100))

def getListingRating(listing):
	try:
		return listing.find("div", {"class": "_1hxyyw3"}).text
	except:
		return ""

def getListingBemerkung(listing):
	try:
		bemerkung = listing.find("div", {"class": "_gxjeqd"}).text
		if "Sehr" in bemerkung:
			bemerkung = bemerkung.split("·")[0]
		return bemerkung
	except:
		return ""

def getListingExtra(listing):
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

def getPersonenAnzahl(listing):
	return listing.find("div", {"class": "_3c0zz1"}).text.split("·")[0]

def getRoomsFromAllUrls(urlArr):
    allRooms = []
    for url in urlArr:
        if url == "":
            break
        pages = getPages(url)
        rooms = getAllRoomClasses(pages)

        allRooms = allRooms + rooms


    return allRooms


def airbnbSearch(urlArr):
	rooms = getRoomsFromAllUrls(urlArr)

	return listingRoomDatatoTable(rooms)

# url_page ="https://www.airbnb.de/s/Costa-Rica/homes?place_id=ChIJJcmsIWLlko8RK5qBNSX3VGI&refinement_paths%5B%5D=%2Fhomes&refinement_path=%2Fhomes&tab_id=home_tab&reset_filters=true&checkin=2021-09-04&checkout=2021-10-05&adults=2&children=1&infants=1&search_type=AUTOSUGGEST"
# url_page2 = ""
# url_page3 = ""
#
# urlArr = [url_page, url_page2, url_page3]
#
#
# rooms = getRoomsFromAllUrls(urlArr)
#
#
# for room in rooms:
# 	print(getListingExtra(room))
