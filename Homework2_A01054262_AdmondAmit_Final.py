# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:32:50 2020

@author: Admond Amit
"""
import pandas as pd
import time 
import re  
from selenium import webdriver
from bs4 import BeautifulSoup
 
#driver = webdriver.Chrome(ChromeDriverManager().install())
PATH    = "/BCIT/Comp2454/Assignments/Assignment2/chromedriver_win32/chromedriver"
URL     = "http://www.uniqueaccommodations.com/"

browser = webdriver.Chrome(PATH)
browser.get(URL)

time.sleep(3) 

# Find the search input.
search  = browser.find_element_by_css_selector("input")                                        
search.send_keys("Vancouver")

# Find the search button - this is only enabled when a search query is entered
button  = browser.find_element_by_css_selector(".id-submit")  
button.click() # Click the button.

# Creating an empty dataframe
propertyDF = pd.DataFrame(columns= ['Rent', 'Address','Area','Bedroom','Bathrooms','Type','Size'])

# start of PropertyEvent Class

class PropertyEvent:
    propertyRent        = ""  # Declare and initialize property rent property.
    propertyAddress     = ""  # Declare and initialize property address property.
    propertyArea        = ""  # Declare and initialize property area property.
    propertyBedroom     = ""  # Declare and initialize property bedroom property.
    propertyBathrooms   = ""  # Declare and initialize property bathrooms property.
    propertyType        = ""  # Declare and initialize property type property.
    propertySize        = ""  # Declare and initialize property size property.

        # Initializing variables for self
    def __init__(self, propertyRent, propertyAddress, propertyArea, propertyBedroom, propertyBathrooms, propertyType, propertySize):
        self.propertyRent        = propertyRent
        self.propertyAddress     = propertyAddress
        self.propertyArea        = propertyArea
        self.propertyBedroom     = propertyBedroom
        self.propertyBathrooms   = propertyBathrooms
        self.propertyType        = propertyType
        self.propertySize        = propertySize

    def showData(self):
        print("Rent: "        + self.propertyRent)
        print("Address: "     + self.propertyAddress)
        print("Area: "        + self.propertyArea)
        print("Bedrooms: "    + self.propertyBedroom)
        print("Bathrooms: "   + self.propertyBathrooms)
        print("Type: "        + self.propertyType)
        print("Size: "        + self.propertySize)
        print("***")

propertyList = [] # Added an empty list.


#Start the loop for 3 page count [NEED TO ADJUST TO 3!]
for i in range(0,3):

# Scrape the search results.                      
  content = browser.find_elements_by_css_selector(".post")   

  for e in content:   
      
      textContent  = e.get_attribute('innerHTML')
    # Beautiful soup removes HTML tags from our content if it exists.
      soup         = BeautifulSoup(textContent, features="lxml")
              
      rawString = soup.get_text().strip()
 
      # Remove hidden characters for tabs and new lines.
      rawString = re.sub(r"[\n\t]*", "", rawString)

      # Replace two or more consecutive empty spaces with '*'

      rawString = re.sub('[ ]{2,}', '*', rawString)

      # Fine tune the results so they can be parsed.

      rawString = rawString.replace("furnished:", "*Rent*")              
      
      rawString = rawString.replace("Available for rent", "*Available for rent*") 
      
      rawString = rawString.replace("Address:", "*Address*")
      
      rawString = rawString.replace("Area:", "*Area*")
      
      rawString = rawString.replace("Neighbourhood:", "*Neighbourhood*")
      
      rawString = rawString.replace("Building:", "*Building*")
      
      rawString = rawString.replace("Bedrooms:", "*Bedrooms*")
      
      rawString = rawString.replace("Bathrooms:", "*Bathrooms*")
      
      rawString = rawString.replace("Property Type:", "*Property Type*")
      
      rawString = rawString.replace("Square Feet:", "*Square Feet*")
      
      rawString = rawString.replace("Pets:", "*Pets*")
 
      rawString = rawString.replace("*/*", "/")

      rawString = rawString.replace("Full*", "*Full*")

      propertyArray = rawString.split('*')

      PROPERTY_RENT       = 2  #OK
      PROPERTY_ADDRESS    = 6  #OK
      PROPERTY_AREA       = 8  #OK
      PROPERTY_BEDROOM    = 14 #OK
      PROPERTY_BEDROOM2   = 15 #string that has "+ Den" if exist
      PROPERTY_BATHROOMS  = 16 #OK
      PROPERTY_BATHROOMS2 = 17 #OK
      PROPERTY_TYPE       = 18 #OK
      PROPERTY_TYPE2      = 19 #OK
      PROPERTY_SIZE       = 20 #OK
      PROPERTY_SIZE2      = 21 #OK
      
      # eliminated the self reference.
      propertyRent          = propertyArray[PROPERTY_RENT].strip()
      propertyAddress       = propertyArray[PROPERTY_ADDRESS].strip()
      propertyArea          = propertyArray[PROPERTY_AREA].strip()
      # start if statement to capture "+ Den" string
      propertyBedroom2      = propertyArray[PROPERTY_BEDROOM2].strip()
      if propertyBedroom2   == "+ Den":      
         propertyBedroom       = propertyArray[PROPERTY_BEDROOM].strip()+' + Den'
      else:
         propertyBedroom       = propertyArray[PROPERTY_BEDROOM].strip()
      propertyBathrooms     = propertyArray[PROPERTY_BATHROOMS].strip()
      if propertyBathrooms  == "Bathrooms":
          propertyBathrooms = propertyArray[PROPERTY_BATHROOMS2].strip()
      # start if statement to capture misalignment of array queue
      propertyType          = propertyArray[PROPERTY_TYPE].strip()
      if propertyType ==  "Property Type":
          propertyType       = propertyArray[PROPERTY_TYPE2].strip()
      # start if statement to capture misalignment of array queue
      propertySize          = propertyArray[PROPERTY_SIZE].strip()
      if propertySize == "Square Feet":
          propertySize       = propertyArray[PROPERTY_SIZE2].strip()

      propertyEvent = PropertyEvent(propertyRent, propertyAddress, propertyArea, propertyBedroom, propertyBathrooms, propertyType, propertySize)
      propertyList.append(propertyEvent)
      # appending property data into dataframe
      propertyDictionary = {'Rent':propertyRent,'Address':propertyAddress,'Area':propertyArea, 'Bedroom':propertyBedroom,'Bathrooms':propertyBathrooms,'Type':propertyType,'Size':propertySize}
      propertyDF = propertyDF.append(propertyDictionary, ignore_index=True)
      
  # Start count for page count scrape
  button = browser.find_element_by_css_selector("#next")
  button.click()
  print("Count: ", str(i))
  time.sleep(4)
    
print("done loop")

for property in propertyList:
    property.showData()
    
print(propertyDF)