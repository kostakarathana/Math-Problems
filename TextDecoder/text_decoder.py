import requests
from bs4 import BeautifulSoup

def decode_secret_message(doc_url):


    response = requests.get(doc_url)
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr")
    grid_map = {}
    max_x = max_y = 0

    for row in rows[1:]:  # Skip the header
        cols = row.find_all("td")
        try:
            x = int(cols[0].get_text(strip=True))
            char = cols[1].get_text(strip=True)
            y = int(cols[2].get_text(strip=True))

            grid_map[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        except ValueError:
            continue
        
    for y in reversed(range(max_y + 1)):
        row = ''
        for x in range(max_x + 1):
            row += grid_map.get((x, y), ' ')
        print(row)

decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")