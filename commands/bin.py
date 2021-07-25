import base64
import collections
import gzip
import io
import time
from json import JSONDecodeError
import item_utils

import dask.bag as db
import requests
import json

from constants import *

blacklist = {"ENCHANTED_BOOK", "PET", "RUNE", "NEW_YEAR_CAKE", "CAKE_SOUL"}


def process_json(json_data):
    bin_prices = {}
    auctions = json_data["auctions"]
    for auction in auctions:
        price = auction["starting_bid"]
        if price < auction["highest_bid_amount"]:
            price = auction["highest_bid_amount"]

        if "bin" in auction and not auction["claimed"] and time.time() * 1000 + 60000 < auction["end"]:
            item_id = item_utils.to_custom_item_id(auction)

            extra = len(auction["extra"][len(auction["item_name"]):].split(" "))
            if item_id not in bin_prices:
                bin_prices[item_id] = []
            auction_data = {
                "uuid": auction["uuid"],
                "price": price,
                "extra": extra,
                "raw": auction
            }
            bin_prices[item_id].append(auction_data)

    return bin_prices


def bin_flip(budget):
    total_pages = requests.get("https://api.hypixel.net/skyblock/auctions?key=" + KEY).json()["totalPages"]
    urls = []
    for page in range(total_pages):
        urls.append("https://api.hypixel.net/skyblock/auctions?key=" + KEY + "&&page=" + str(page))

    datas = db.read_text(urls).map(json.loads).map(process_json).compute()
    bin_prices = {}
    for data in datas:
        for key in data.keys():
            if key not in bin_prices.keys():
                bin_prices[key] = []
            bin_prices[key] += data[key]
    best_flip = {}
    for key in bin_prices.keys():
        bin_prices[key] = sorted(bin_prices[key], key=lambda row: row["price"])
        if len(bin_prices[key]) >= BIN_ITEM_LIMIT:
            selling_price = bin_prices[key][1]["price"]
            buying_price = bin_prices[key][0]["price"]
            profit = selling_price * 0.99 - buying_price
            if buying_price < budget and bin_prices[key][0]["extra"] <= bin_prices[key][1]["extra"]:
                best_flip[(key, bin_prices[key][0]["uuid"], buying_price, selling_price)] = profit

    counter = collections.Counter(best_flip)

    return counter.most_common(15)
