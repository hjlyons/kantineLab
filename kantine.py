#!/usr/bin/env python3
# Script for scraping DESY kantine information
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import datetime

# To map numbers to low, medium, high colour scheme
calorieMap = {}
priceMap = {}


# Kantine URL
kantine_url = 'https://desy.myalsterfood.de/'
# YYYY-MM-DD regex
reg_pattern = "^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"

def dateFilter(menutag):
    date_time_obj = datetime.datetime.strptime(menutag.get('id'), '%Y-%m-%d')
    # Filter out only todays date
    if date_time_obj.date() == datetime.date.today():
        return True
    # Show all, with past filtered out
    # if date_time_obj.date() >= datetime.date.today():
    #    return True
    # Show all
    # else:
    #    return True   
    return False

def parseMenu(menutag):
    print("\n" + "-"*40 + "  " + menutag.get('id') + "  " + "-"*40)
    menu_items = [tag for tag in menutag.find_all("table", {"class" : re.compile('food-item')})]
    for meal in menu_items:
        # English phrases held in grey-text, most likely instance to break if webpage redesigned
        engSpans = meal.find_all("span", {"class" : re.compile('grey-text')})
        priceSpan = meal.find_all("span", {"class" : re.compile('price-text')})
        priceFloat = float(priceSpan[0].text.replace('€ ', '').replace(',','.'))

        if "Main" not in engSpans[0].text:
            continue  
        if ("vegan" in engSpans[2].text) or ("vegetarian" in engSpans[2].text):
            print(engSpans[1].text) 
            print("Price: " +  str(priceFloat))


    print("="*94)

with urlopen(kantine_url) as response:
    soup = BeautifulSoup(response, 'html.parser')
    
    # Finds the menu for each date, filter out ones in past
    day_menus = soup.find_all("div", id=re.compile(reg_pattern))
    day_menus = [menu for menu in day_menus if dateFilter(menu)]

    for i, tag in enumerate(day_menus):
        parseMenu(tag)


    print("\n")