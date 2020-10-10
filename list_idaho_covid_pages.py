#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://public.tableau.com/views/DPHIdahoCOVID-19Dashboard/Home"

r = requests.get(
    url,
    params= {
        ":showVizHome":"no",
    }
)
soup = BeautifulSoup(r.text, "html.parser")

tableauData = json.loads(soup.find("textarea",{"id": "tsConfigContainer"}).text)

dataUrl = f'https://public.tableau.com{tableauData["vizql_root"]}/bootstrapSession/sessions/{tableauData["sessionid"]}'

r = requests.post(dataUrl, data= {
    "sheet_id": tableauData["sheetId"],
})

dataReg = re.search('\d+;({.*})\d+;({.*})', r.text, re.MULTILINE)
info = json.loads(dataReg.group(1))

sheetsinfo = info['worldUpdate']['applicationPresModel']['workbookPresModel']['sheetsInfo']

print("sheet,subsheet")
for sheet in sheetsinfo:
	if not sheet['isPublished']:
		continue
	for subsheet in sheet['namesOfSubsheets']:
		print("%s,%s" % (sheet['sheet'], subsheet))

