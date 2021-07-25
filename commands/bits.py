import base64
import collections
import gzip
import io

import dask.bag as db
import requests
import json
from main import KEY


def process_json(json_data):
    bin_prices = {}

    auctions = json_data["auctions"]
    for auction in auctions:
        price = auction["starting_bid"]
        if price < auction["highest_bid_amount"]:
            price = auction["highest_bid_amount"]

        item_id = ""

        raw_nbt_data = gzip.GzipFile(fileobj=io.BytesIO(base64.b64decode(auction["item_bytes"]))).read().decode(
            "ISO-8859-1")

        field = ""
        i = len(raw_nbt_data) - 1
        while True:
            if raw_nbt_data[i] < ' ':
                if field == "di":
                    break
                field = ""
            else:
                field += raw_nbt_data[i]

            i -= 1
        i += 5
        c = raw_nbt_data[i]
        while ord(c) >= 20:
            item_id += c
            i += 1
            c = raw_nbt_data[i]

        if "bin" in auction:
            if item_id not in bin_prices:
                bin_prices[item_id] = price
            if price > bin_prices[item_id]:
                bin_prices[item_id] = price

    return bin_prices


def bestbits(bits):
    total_pages = \
        requests.get("https://api.hypixel.net/skyblock/auctions?key=" + KEY).json()[
            "totalPages"]
    urls = []
    for page in range(total_pages):
        urls.append(
            "https://api.hypixel.net/skyblock/auctions?key=" + KEY + "&&page=" + str(page))

    datas = db.read_text(urls).map(json.loads).map(process_json).compute()
    prices = {}
    for data in datas:
        for key in data.keys():
            if key not in prices:
                prices[key] = data[key]
            if prices[key] > data[key]:
                prices[key] = data[key]
    bit_items = {
        "God Potion": ["GOD_POTION2", 1500],
        "Kat Flower": ["KAT_FLOWER", 500],
        "Heat Core": ["HEAT_CORE", 3000],
        "Hyper Catalyst Upgrade": ["HYPER_CATALYST_UPGRADE", 300],
        "Ultimate Carrot Candy Upgrade": ["ULTIMATE_CARROT_CANDY_UPGRADE", 8000],
        "Colossal Exp Bottle": ["COLOSSAL_EXP_BOTTLE_UPGRADE", 1200],
        "Jumbo Backpack Upgrade": ["JUMBO_BACKPACK_UPGRADE", 4000],
        "Minion Storage Expander": ["MINION_STORAGE_EXPANDER", 1500],
        "Hologram": ["HOLOGRAM", 2000],
        "Dungeon Sack": ["LARGE_DUNGEON_SACK", 10000],
        "Builders Wand": ["BUILDERS_WAND", 12000],
        "Block Zapper": ["BLOCK_ZAPPER", 5000],
        "Bits Talisman": ["BITS_TALISMAN", 15000],
        "Rune Sack": ["RUNE_SACK", 10000],
        "Autopets Rule": ["AUTOPET_RULES_2", 21000],
        "Kismet Feather": ["KISMET_FEATHER", 1350],
        "Speed Enrichment": ["TALISMAN_ENRICHMENT_WALK_SPEED", 5000],
        "Intelligence Enrichment": ["TALISMAN_ENRICHMENT_INTELLIGENCE", 5000],
        "Critical Chance Enrichment": ["TALISMAN_ENRICHMENT_CRITICAL_CHANCE", 5000],
        "Critical Damage Enrichment": ["TALISMAN_ENRICHMENT_CRITICAL_DAMAGE", 5000],
        "Strength Enrichment": ["TALISMAN_ENRICHMENT_STRENGTH", 5000],
        "Defense Enrichment": ["TALISMAN_ENRICHMENT_DEFENSE", 5000],
        "Health Enrichment": ["TALISMAN_ENRICHMENT_HEALTH", 5000],
        "Magic Find Enrichment": ["TALISMAN_ENRICHMENT_MAGIC_FIND", 5000],
        "Ferocity Enrichment": ["TALISMAN_ENRICHMENT_FEROCITY", 5000],
        "Sea Creature Chance Enrichment": ["TALISMAN_ENRICHMENT_SEA_CREATURE_CHANCE", 5000],
        "Enrichment swapper": ["TALISMAN_ENRICHMENT_SWAPPER", 200]
    }
    items_bought = {}
    total_profit = 0
    while bits >= 200:
        best_item = "god potion"
        best_coins_per_bit = 0
        for key in bit_items:
            if bit_items[key][0] in prices:
                coins_per_bits = prices[bit_items[key][0]]/bit_items[key][1]
                if coins_per_bits > best_coins_per_bit:
                    best_item = key
                    best_coins_per_bit = coins_per_bits
        if best_item not in items_bought:
            items_bought[best_item] = 0
        items_bought[best_item] += 1
        total_profit += prices[bit_items[best_item][0]]
        bits -= bit_items[best_item][1]
        prices[bit_items[best_item][0]] *= 0.99
    return total_profit, items_bought
