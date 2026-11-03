# Web Scraping with Python Assignment

The wiki I am choosing to work with for this project is the Minecraft Wiki.

Link to robots.txt file: https://minecraft.wiki/robots.txt

Some of the AI it forbids from the site includes:
- Perplexity
- OAI Searchbot
- AmazonProductDiscoveryBot
- Claude related bots
- Some google-related bots

## Data I will be scraping: Trades in Minecraft

One thing that I always found tricky as a player in Minecraft was understanding the trading system. For anyone unfamiliar, villagers are a mob in Minecraft that are stand-ins for NPCs, and they offer a variety of resources purchased through their currency of emeralds, and some unique items. This mechanic is called trading. Additionally when I played the game, one feature I remember about villagers is that they are stingy about trades and will make cost-effective trades for themselves.

My questions I wish to solve with this project are: 
- Which items are cheapest and most expensive per unit in villager trades, measured in emeralds?
- For items that villagers both buy and sell, how large is the gap between the two prices? In other words, how much is the player getting ripped off for?

## My method for web-scraping

The main Trading page on the minecraft wiki is setup with clear headers, and contains the information we need to scrap 2nd level information regarding trades. 

To get individual trade data which will be the starting point for the data in our csv, I first run a check of each header to find where 'Trade Offers' begins. I also check for where 'Wandering Villager Trades' header starts, as I will be omitting wandering villager trades from this dataset. (Mechanically, they tend to offer only single emerald trades for items unique to only their character, and do not give out emeralds which messes with the second part of our research question.)