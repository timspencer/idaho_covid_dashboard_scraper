# Idaho COVID-19 dashboard scraper

These scripts can be used to get access to the data behind the Idaho 
[COVID-19 Data Dashboard](https://public.tableau.com/views/DPHIdahoCOVID-19Dashboard/Home).

You can always go to the bottom of the page and click on "Download" yourself, but this
does not work for an automated scraper which can be used to incorporate this data into
another system.  These scripts do that for you.

# Install

You will need to have python3 installed on your system.
https://wiki.python.org/moin/BeginnersGuide/Download

`pip3 install -r requirements.txt` will install all of the python dependencies.

# Usage

```
./list_idaho_covid_pages.py > id_covid_sheets.csv
```
This will create a CSV file that has all of the sheets and subsheets in it.
You can use this to automate scraping all of the sheets and enumerate what
you can look at.

```
./scrape_idaho_covid_data.py sheet subsheet > id_sheet_subsheet.csv
```
This will pull the data down from `sheet` and `subsheet` and put it in a csv file.
If it cannot pull the data down, it will exit with a non-zero status.

# Caveats

These scripts are potentially fragile.  Tableau seems to be trying to provide a way for
people to pull data out (https://github.com/tableau/server-client-python), but this does
not work against a public server, so I had to reverse-engineer how it works by looking at
the URLs and data that they emitted while clicking on the download links.

YMMV

