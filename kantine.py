#!/usr/bin/env python3
# Script for scraping DESY kantine information
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import datetime

class bcolors:
    HEADER = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# To map numbers to low, medium, high colour scheme
priceLow = 4.20
priceHigh = 5.00
kcalLow = 700
kcalHigh = 900

# Kantine URL
kantine_url = 'https://desy.myalsterfood.de/'
# YYYY-MM-DD regex
reg_pattern = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"


def priceToColor(price):
    if price < priceLow:
        return bcolors.GREEN
    elif price > priceHigh:
        return bcolors.RED
    else:
        return bcolors.YELLOW

def kcalToColor(kcal):
    if kcal < kcalLow:
        return bcolors.GREEN
    elif kcal > kcalHigh:
        return bcolors.RED
    else:
        return bcolors.YELLOW

def dateFilter(menutag):
    date_time_obj = datetime.datetime.strptime(menutag.get('id'), '%Y-%m-%d')
    # Filter out only todays date
    #if date_time_obj.date() >= datetime.date.today():
    #    return True
    # Show all, with past filtered out
    # if date_time_obj.date() >= datetime.date.today():
    #    return True
    # Show all
    # else:
    #    return True   
    return True

def dateToday(menutag):
    date_time_obj = datetime.datetime.strptime(menutag.get('id'), '%Y-%m-%d')
    if date_time_obj.date() == datetime.date.today():
        return True 
    return False

def parseMenu(menutag):
    indent = ""
    if dateToday(menutag):
        indent = " "*42
    print(bcolors.BOLD +  "\n" + indent + "-"*40 + "  " + menutag.get('id') + "  " + "-"*40 + bcolors.ENDC)
    menu_items = [tag for tag in menutag.find_all("table", {"class" : re.compile('food-item')})]
    if menu_items:
        for meal in menu_items:
            # English phrases held in grey-text, most likely instance to break if webpage redesigned
            engSpans = meal.find_all("span", {"class" : re.compile('grey-text')})
            priceSpan = meal.find_all("span", {"class" : re.compile('price-text')})
            if meal.find_all("div", {"class" : re.compile('modal-content')}):
                ingredientsText = meal.find_all("div", {"class" : re.compile('modal-content')})[0].find("p").getText()
                ingredientsText = ingredientsText.split('\n')[1].strip()
                kcalFloat = float(ingredientsText.split(' ')[-2].replace('.',''))

            if priceSpan:
                priceFloat = float(priceSpan[0].text.replace('€ ', '').replace(',','.'))

            if "Main" not in engSpans[0].text:
                continue  
            if ("vegan" in engSpans[2].text) or ("vegetarian" in engSpans[2].text):
                print(indent + engSpans[1].text) 
                print(indent + priceToColor(priceFloat) + "Price (EUR): %.2f" % priceFloat + bcolors.ENDC)
                if ingredientsText:
                    print(indent + kcalToColor(kcalFloat) + "kCal: %s" % kcalFloat + bcolors.ENDC)
   
    print(indent + "="*94)

with urlopen(kantine_url) as response:
    soup = BeautifulSoup(response, 'html.parser')
    
    # Finds the menu for each date, filter out ones in past
    day_menus = soup.find_all("div", id=re.compile(reg_pattern))
    day_menus = [menu for menu in day_menus if dateFilter(menu)]

    for i, tag in enumerate(day_menus):
        parseMenu(tag)


    print("\n")
