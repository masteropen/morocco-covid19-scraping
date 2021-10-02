from bs4 import BeautifulSoup
import requests
import json
import os

url = "https://fr.wikipedia.org/wiki/Pand%C3%A9mie_de_Covid-19_au_Maroc#D%C3%A9veloppement_du_virus"
export_dir = "export/wikipedia"
export_file_name = "data.json"

if not os.path.exists(export_dir):
    os.makedirs(export_dir)

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
crawledTables = soup.find_all('table')
items = crawledTables[3].text.split("\n\n")


def format_data(element):
    if type(element) is str:
        return element.replace("\n", "")
    elif type(element) is list:
        data = []
        for item in element:
            data.append(item.encode("ascii", "ignore").decode())
        return data
    else:
        return 'error format'


def get_columns(elements: list):
    return {
        "total_tests": elements[0],
        "negatives": elements[1],
        "positives": elements[2],
        "deaths": elements[3],
        "reestablishes": elements[4],
        "new_cases": elements[5],
    }


formatted_data = []
for index, inf in enumerate(items):
    if index == 9:
        formatted_data.append({"date": format_data(inf), "data": get_columns(format_data(items[index + 1: index + 7]))})
    elif inf.startswith("\n") and index > 9:
        formatted_data.append({"date": format_data(inf), "data": get_columns(format_data(items[index + 1: index + 7]))})
    else:
        continue

with open(export_dir+"/"+export_file_name, "w") as f:
    json.dump(formatted_data, f)
