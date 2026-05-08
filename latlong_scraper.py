import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.google.com/search?q="
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_coordinates(sector):
    try:
        search_term = f"sector {sector} gurgaon longitude & latitude"
        response = requests.get(BASE_URL + search_term, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Note: Google changes classes often; this might return None
            coordinates_div = soup.find("div", class_="Z0LcW") 
            return coordinates_div.text if coordinates_div else "Not Found"
    except Exception as e:
        return None

results = []
for sector in range(1, 116):
    coords = get_coordinates(sector)
    results.append({"Sector": f"Sector {sector}", "Coordinates": coords})
    time.sleep(1) # Delay to prevent getting blocked

df = pd.DataFrame(results)
df.to_csv("gurgaon_sectors_coordinates.csv", index=False)