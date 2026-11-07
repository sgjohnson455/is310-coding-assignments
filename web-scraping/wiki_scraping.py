import csv
import re
import time

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

# Project Constants -----
BASE_URL = "https://minecraft.wiki"
MOBS_URL = f"{BASE_URL}/w/Mob"

REQUEST_DELAY = 1.0       

OUTPUT = "minecraft_mobs.csv"

console = Console()

#Introduce ourselves ----
HEADERS = {"User-Agent": "is310-course-scraper/1.0 (student project; sjohn241@illinois.edu)"}

#csv field names
FIELDNAMES = ["mob", "url", "spawn_description"]

# Functions ---------------------

# Takes URL as parameter, download page, and return BeautifulSoup object (else return None)
def fetch_soup(url):
    if not url:
        console.print("[yellow]No URL was found for this page.[/yellow]")
        return None

    response = requests.get(url, headers=HEADERS, timeout=30)
    time.sleep(REQUEST_DELAY)

    if response.status_code != 200:
        console.print(f"[red]Could not download {url}: HTTP {response.status_code}[/red]")
        return None

    return BeautifulSoup(response.text, "html.parser")

def is_next_section(tag):
    classes = tag.get("class") or []
    if tag.name == "h2" or "mw-heading2" in classes:
        return True
    return False
    
def get_spawn_text(soup):
    header = soup.find(id="Spawning")
    if header is None:
        return None   # this page has no Spawning section
    start = header.find_parent("div", class_="mw-heading") or header

    parts = []

    # append text until we hit another header
    for sibling in start.find_next_siblings():
        if is_next_section(sibling):      # next header of any level: stop
            break
        text = sibling.get_text(" ", strip=True)
        if text:
            parts.append(text)

    # return the spawn text joined, or simply return None
    if parts:
        return " ".join(parts)
    else:
        return None
    
# save records to the csv 
def save_csv(records, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)

# MAIN CODE ---------------------------

# main data
soup = fetch_soup(MOBS_URL)
mob_links = []
seen = set()
records = []

correct_range = False

# First level scraping: obtaining a link for each mob on the mobs page (that is applicable)

if soup is None:
    console.print("[red]Fetched page is empty[/red]")
else:
    for element in soup.find_all(["h2", "h3", "h4", "a"]):

        # get correct range for element search ---------------
        if element.name != "a":
            title = element.get_text(" ", strip=True)
            if title == "List of mobs":
                correct_range = True
            elif title == "Upcoming mobs":
                break
            continue
        if not correct_range:
            continue

        # find the name link inside each mob
        if element.find_parent("div", class_="mob-name") is None:
            continue
        href = element["href"] if element.has_attr("href") else None
        if not href or not href.startswith("/w/") or ":" in href:
            continue
        if "Mentioned_features" in href: # they have some placeholder mobs in there
            continue

        # append url of mob link
        url = BASE_URL + href.split("#")[0] # url pattern uses a # as a seperator
        if url not in seen:
            seen.add(url)
            mob_links.append([element.get_text(strip=True), url])

    


# Second level scraping: visiting each page and getting the spawning info from them

#for name, url in mob_links:
for name, url in mob_links:
    console.print(f"Scraping {name}...") # let me know which mob is being scraped
    mob_soup = fetch_soup(url)
    if mob_soup is None:
        continue
    records.append({
        "mob": name,
        "url": url.split("#")[0],
        "spawn_description": get_spawn_text(mob_soup),
    })
    
save_csv(records, OUTPUT)
console.print(f"Saved {len(records)} mobs to {OUTPUT}")
