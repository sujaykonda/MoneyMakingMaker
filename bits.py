import base64
import collections
import gzip
import io

import dask.bag as db
import requests
import json


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


def coin_per_bits():
    total_pages = \
        requests.get("https://api.hypixel.net/skyblock/auctions?key=60b5fe52-8f17-432d-9f90-7fa79ae63ed5").json()[
            "totalPages"]
    urls = []
    for page in range(total_pages):
        urls.append(
            "https://api.hypixel.net/skyblock/auctions?key=60b5fe52-8f17-432d-9f90-7fa79ae63ed5&&page=" + str(page))

    datas = db.read_text(urls).map(json.loads).map(process_json).compute()
    prices = {}
    for data in datas:
        for key in data.keys():
            if key not in prices:
                prices[key] = data[key]
            if prices[key] > data[key]:
                prices[key] = data[key]
    print(prices)
    bitcost = {
        "god potion": ["GOD_POTION", 1500],
        "kat flower": ["KAT_FLOWER", 500],
        "heat core": ["HEAT_CORE", 3000],
        "hyper catalyst upgrade": ["HYPER_CATALYST_UPGRADE", 300],
        "ultimate carrot candy upgrade": ["ULTIMATE_CARROT_CANDY_UPGRADE", 8000],
        "colossal exp bottle": ["COLOSSAL_EXP_BOTTLE_UPGRADE", 1200],
        "jumbo backpack upgrade": ["JUMBO_BACKPACK_UPGRADE", 4000],
        "minion storage expander": ["MINION_STORAGE_EXPANDER", 1500],
        "hologram": ["HOLOGRAM", 2000],
        "dungeon sack": ["LARGE_DUNGEON_SACK", 10000],
        "builders wand": ["BUILDERS_WAND", 12000],
        "block zapper": ["BLOCK_ZAPPER", 5000],
        "bits talisman": ["BITS_TALISMAN", 15000],
        "rune sack": ["RUNE_SACK", 10000],
        "autopets rule": ["AUTOPET_RULES_2", 21000],
        "kismet feather": ["KISMET_FEATHER", 1350],
        "speed enrichment": ["TALISMAN_ENRICHMENT_WALK_SPEED", 5000],
        "intelligence enrichment": ["TALISMAN_ENRICHMENT_INTELLIGENCE", 5000],
        "critical chance enrichment": ["TALISMAN_ENRICHMENT_CRITICAL_CHANCE", 5000],
        "critical damage enrichment": ["TALISMAN_ENRICHMENT_CRITICAL_DAMAGE", 5000],
        "strength enrichment": ["TALISMAN_ENRICHMENT_STRENGTH", 5000],
        "defense enrichment": ["TALISMAN_ENRICHMENT_DEFENSE", 5000],
        "health enrichment": ["TALISMAN_ENRICHMENT_HEALTH", 5000],
        "magic find enrichment": ["TALISMAN_ENRICHMENT_MAGIC_FIND", 5000],
        "ferocity enrichment": ["TALISMAN_ENRICHMENT_FEROCITY", 5000],
        "sea creature chance enrichment": ["TALISMAN_ENRICHMENT_SEA_CREATURE_CHANCE", 5000],
        "enrichment swapper": ["TALISMAN_ENRICHMENT_SWAPPER", 200],
    }