# Marvel Rivals Tierlist: CLI Homework

This project

## It collects

Each record describes one hero and their respective ranking:

| Field | Description |
|---|---|
| `Hero Name` | The name of the hero in Marvel Rivals |
| `Tier List Rank` | The letter of their tierlist ranking (C-S) |
| `Hero Role` | Role of the hero in the game |

## Install

The CLI uses the [Rich](https://rich.readthedocs.io/) library. From the project folder, run:

```
pip install -r requirements.txt
```

The HTML version needs no installation.

## Run the CLI

```
python3 cli_data_entry.py
```

1. The script shows some example rankings taken from a game leaderboard
2. The script then takes in the hero name, tier ranking, and game role of a new hero
3. It then updates the csv with that information and displays the new table to the user.
4. It asks if you want to add more data, and if not, ends the program.
