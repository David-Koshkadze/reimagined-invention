import requests
from bs4 import BeautifulSoup
import json
import csv

URL = "https://www.worldometers.info/coronavirus/"

response = requests.get(URL)

soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", id="main_table_countries_today")

rows = table.find_all("tr")

data = []

for row in rows:
    cells = row.find_all("td")

    if len(cells) > 0:
        country = cells.find('td', class_="listing_1").text
        total_cases = cells[1].text.strip()
        total_deaths = cells[3].text.strip()
        total_recovered = cells[5].text.strip()

        country_data = {
            "country": country,
            "total_cases": total_cases,
            "total_deaths": total_deaths,
            "total_recovered": total_recovered
        }

        data.append(country_data)

json_data = json.dumps(data, indent=4)

with open('data.csv', mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Total Cases", "Total Deaths", "Total Recovered"])  
    for item in data:
        writer.writerow([item["country"], item["total_cases"], item["total_deaths"], item["total_recovered"]])

print("Data saved to", 'data.csv')

print(json_data)
