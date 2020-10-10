#!/usr/bin/env python3
#
# This script downloads the data from the specified sheet and subsheet on the
# Idaho COVID-19 Data dashboard.  It is kinda fragile, in that all this session
# and view ID stuff is totally undocumented by the tableau people in any way
# that I was able to find, so if they change their system, it will break.  I
# just figured it out by looking at the data and URLs.
#
# That said, people generally don't seem to change these kinds of things very
# often, so it'll probably work forever.

import requests
from bs4 import BeautifulSoup
import json
import re
import sys

if len(sys.argv) < 3:
    print(f"usage:  {sys.argv[0]} <sheet> <subsheet>")
    sys.exit(1)

sheet = sys.argv[1]
subsheet = sys.argv[2]
url = "https://public.tableau.com/views/DPHIdahoCOVID-19Dashboard/" + sheet

r = requests.get(
    url,
    params={
        ":showVizHome": "no",
    }
)
if r.status_code != 200:
    print(f"{sheet} does not seem to be a valid sheet")
    sys.exit(2)

soup = BeautifulSoup(r.text, "html.parser")
tableauData = json.loads(soup.find("textarea",
                         {"id": "tsConfigContainer"}).text)
dataUrl = f'https://public.tableau.com{tableauData["vizql_root"]}/bootstrapSession/sessions/{tableauData["sessionid"]}'

r = requests.post(dataUrl, data={
    "sheet_id": tableauData["sheetId"],
})
if r.status_code != 200:
    print(f"could not create session with tableau")
    sys.exit(2)

dataReg = re.search('\d+;({.*})\d+;({.*})', r.text, re.MULTILINE)
info = json.loads(dataReg.group(1))

session_id = info['newSessionId']
try:
    view_id = info['worldUpdate']['applicationPresModel']['workbookPresModel']['dashboardPresModel']['viewIds'][subsheet]
except:
    print(f"{subsheet} does not seem to be a valid subsheet")
    sys.exit(2)

downloadurl = f'https://public.tableau.com{tableauData["vizql_root"]}/vudcsv/sessions/{session_id}/views/{view_id}'

r = requests.get(downloadurl,
                 params={
                     "underlying_table_id": "Migrated%20Data",
                     "underlying_table_caption": "Full%20Data"
                 })
if r.status_code != 200:
    print(f"error downloading data for {sheet} {subsheet}")
    sys.exit(2)

print(r.text)
