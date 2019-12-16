#!/usr/bin/env python3
# Anchor extraction from HTML document
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import datetime

# Cantine URL
cantine_url = 'https://desy.myalsterfood.de/'
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

def menuToVeggie(menutag):
    print("Parsing menu for: %s" % menutag.get('id'))

with urlopen(cantine_url) as response:
    soup = BeautifulSoup(response, 'html.parser')
    
    # Finds the menu for each date, filter out ones in past
    day_menus = soup.find_all("div", id=re.compile(reg_pattern))
    day_menus = [menu for menu in day_menus if dateFilter(menu)]

    for i, tag in enumerate(day_menus):
        menuToVeggie(tag)