from rich.console import Console
from rich.table import Table
import csv

headers = ['Hero', 'Tierlist Rank', 'Role']
starter_data = [
    ['Peni Parker', 'S', 'Vanguard'],
    ['Jubilee', 'A', 'Strategist'],
    ['Starlord', 'B', 'Duelist']
]

console = Console()

#Initialize Table
table = Table(title="Marvel Rivals Hero Tierlist")

#Add table columns
table.add_column("Hero Name", style="magenta")
table.add_column("Tier", style="cyan", no_wrap=True)
table.add_column("Role", justify="left")

#write out rows from the csv to the table in cli
with open('marvelRivalsTiers.csv', mode='r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        print(row)
        table.add_row(row[0], row[1], row[2])

# print out initial input 
console.print(table)

# -- CLI input assingment

continue_input = 'Y'

# Open file to write to

while (continue_input == 'Y'):
    print("Add your hero rankings")
    hero_name = input("Hero Name: ")
    tier_list_rank = input("Enter hero tier (C,B,A,S): ")
    hero_role = input("Hero Role (Vanguard/Duelist/Strategist): ")
    
    tier_list_entry = [hero_name, tier_list_rank, hero_role]
    
    #open and write entry to csv
    with open('marvelRivalsTiers.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(tier_list_entry)
   

    #add entry visually to table
    table.add_row(hero_name, tier_list_rank, hero_role)

    #print table
    console.print(table)
    
    print("Thanks for contributing data to the tierlist. Your information has been stored locally to a csv in this project.")
    continue_input = input("Add more data? (Y/N): ")

    print("You can close this program now.")


