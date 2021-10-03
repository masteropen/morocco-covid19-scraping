# note: cannot scrap and crawl almost of time the hespress DOM
# so we use Wikipedia data to retrieve Morocco covid 19 data

from bs4 import BeautifulSoup
import requests
import os


url = "https://fr.hespress.com/227118-coronavirus-maroc-casablanca-et-rabat-les-plus-touchees-par-de-nouveaux-cas-2.html"
export_dir = "export/hespress"
export_file_name = "data.csv"

if not os.path.exists(export_dir):
    os.makedirs(export_dir)

formatted_data = []
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
titles = soup.find_all('h1')
navs = soup.find_all('nav')
imgs = soup.find_all('img')
title = titles[0].text
category = navs[1].text
content = navs[29].text

formatted_data.append(title)
formatted_data.append(category.replace("\n\n\n", " ").replace("\n", "").lstrip(" ").rstrip(" "))
formatted_data.append(content)

textfile = open(export_dir+"/"+export_file_name, "w")
for element in formatted_data:
    textfile.write(" ".join(element)+"\n")
textfile.close()
