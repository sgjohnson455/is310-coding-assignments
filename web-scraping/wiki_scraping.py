import csv
import re
import time

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

# Project Constants -----
BASE_URL = "https://minecraft.wiki"
TRADING_URL = f"{BASE_URL}/w/Trading"

REQUEST_DELAY = 1.0       
MAX_ITEM_PAGES = 10   # testing this
EXCLUDE_ITEMS = {"Emerald"}  # emeralds mentioned a lot in these tables

OUTPUT = "web-scraping/minecraft_trades.csv"

console = Console()

#Introduce ourselves ----
HEADERS = {"User-Agent": "is310-course-scraper/1.0 (student project; sjohn241@illinois.edu)"}
#response = requests.get("https://minecraft.wiki/w/Trading", headers=HEADERS, timeout=10)

#Site is in fact active: 200
#print(response.status_code)

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

# Function: Finds the tables containing trades on the main trading page
def find_trade_tables(soup):
    parsed_trades = [] 
    in_trade_offers = False # true if we are between headers for trade offers and wandering trader
    profession = None

    for element in soup.find_all(["h2", "h3", "h4", "table"]):
        if element.name == "table":
            # check if in header range + table is correct (trade tables have 'Villager wants' text)
            if in_trade_offers and "Villager wants" in element.get_text():
                parsed_trades.append((profession, element))
            continue

        title = element.get_text(" ", strip=True)

        # Before the section starts: ignore everything until "Trade offers"
        if not in_trade_offers:
            if title.startswith("Trade offers"):
                in_trade_offers = True
            continue

        # Inside the section: stop at the Wandering Trader or the next top-level section
        if title.startswith("Wandering Trader"):
            break
        if element.name == "h2":
            break

            # tag our trade with the profession of the table it comes from 
        profession = title

    return parsed_trades

# for parsing cells - handles cases where items may have ranges
def parse_item_cell(cell):
    """Return (text, quantity, item_names). A range like '19–33 ×' becomes its average."""
    text = cell.get_text(" ", strip=True)
    match = re.match(r"(\d+)(?:\s*[–-]\s*(\d+))?\s*×", text)

    if match:
        low = int(match.group(1))
        high = int(match.group(2)) if match.group(2) else low
        quantity = (low + high) / 2
        if quantity.is_integer():
            quantity = int(quantity)
    else:
        quantity = 1

    names = [span.get_text(strip=True) for span in cell.find_all("span", class_="sprite-text")]
    return text, quantity, names

# gets info for prices
def get_price_info(wants_qty, wants_names, gets_qty, gets_names):
    """Emerald price of ONE unit, for simple item <-> emerald trades."""
    if wants_names == ["Emerald"] and len(gets_names) == 1 and gets_names[0] != "Emerald":
        return "player_buys", gets_names[0], round(wants_qty / gets_qty, 5)
    if gets_names == ["Emerald"] and len(wants_names) == 1 and wants_names[0] != "Emerald":
        return "player_sells", wants_names[0], round(gets_qty / wants_qty, 5)
    return "other", "", None

# save info to a csv
def save_csv(records, output_path):
    if not records:
        console.print(f"[yellow]No records to save to {output_path}[/yellow]")
        return

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


# MAIN CODE ---------------------------

# main data
tables = [] # stores the names of the tables
trades = []


trading_soup = fetch_soup(TRADING_URL)

print(trading_soup)

if trading_soup is None:
    print("Fetched page is empty") # do nothing
else:
    #print(trading_soup.title.get_text()) # check page output
    

    for element in trading_soup.find_all(["h2", "h3", "h4"]):
        print(element.name, "|", element.get_text(" ", strip=True))





    # # get initial tables
    # for table in trading_soup.find_all("table"):
    #     if "Villager wants" in table.get_text():
    #         tables.append(table)

    # for table in tables:
    #     heading = table.find_previous(["h2", "h3", "h4"])
    #     profession = heading.get_text(" ", strip=True)
    #     level = None

    #     for row in table.find_all("tr"):
    #         # the level lives in a <th>; remember it for rows that omit it
    #         th = row.find("th")
    #         if th is not None:
    #             level = th.get_text(" ", strip=True)

    #         cells = row.find_all("td")
    #         if len(cells) != 7:
    #             continue

    #         wants_text, wants_qty, wants_names = parse_item_cell(cells[2])
    #         gets_text, gets_qty, gets_names = parse_item_cell(cells[3])
    #         direction, item, price = get_price_info(wants_qty, wants_names, gets_qty, gets_names)

    #         trades.append({
    #             "profession": profession,
    #             "level": level,
    #             "wants": wants_text,
    #             "receives": gets_text,
    #             "direction": direction,
    #             "item": item,
    #             "emerald_price_per_unit": price,
    #         })

    # print(f"Collected {len(trades)} trades")
    # print(trades[:3])

    # save_csv(trades, OUTPUT)
    # console.print(f"[green]Saved {len(trades)} trades to {OUTPUT}[/green]")
    