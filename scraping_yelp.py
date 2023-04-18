# https://www.yelp.careers/us/en and https://www.yelp.careers/us/en/search-results
#scraping above links for jobs

import os
import requests
from bs4 import BeautifulSoup
import json
import openpyxl
import textwrap

#using proxy
proxy = "http://melab1:rgukt12345@staffnet.rgukt.ac.in:3128"
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy 

r = requests.get("https://www.yelp.careers/us/en/search-results")
soup = BeautifulSoup(r.content,"html.parser")
script = str(soup.find("script")) 

li = []
li2 = []
br_c = 0
#converting the string to proper dictionary format
for word in script:
   if(word=='{'):
      br_c+=1
   elif(word=='}'):
      br_c-=1
   li.append(word)
   if(br_c==0):
      st = ""
      li2.append(st.join(li))
      li.clear()
      
data = json.loads(li2[79])
li = data["eagerLoadRefineSearch"]["data"]["jobs"]  #jobs data

wb = openpyxl.Workbook()
sheet = wb.active 
#titles
sheet.column_dimensions['A'].width = 50
sheet["A1"] = "TITLE"
sheet.column_dimensions['B'].width = 40
sheet["B1"] = "ADDRESS"
sheet.column_dimensions['C'].width = 50
sheet["C1"] = "APPLY URL"
sheet.column_dimensions['D'].width = 30
sheet["D1"] = "POSTED DATE"
sheet.column_dimensions['E'].width = 100
sheet["E1"] = "DESCRIPTION TEASER"
count = 2
for item in li:
   sheet["A"+str(count)] = item["title"]
   sheet["B"+str(count)] = item["address"]
   sheet["C"+str(count)] = item["applyUrl"]
   sheet["D"+str(count)] = item["postedDate"]
   sheet["E"+str(count)] = item["descriptionTeaser"]
   count+=1
wb.save('output.xlsx')
