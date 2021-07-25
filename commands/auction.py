import base64
import collections
import gzip
import io
import item_utils

import dask.bag as db
import requests
import json
import time
from constants import *

blacklist = {"ENCHANTED_BOOK", "PET", "RUNE", "NEW_YEAR_CAKE"}


def process_json(json_data):
    auction_prices = {}
    bin_prices = {}

    auctions = json_data["auctions"]
    for auction in auctions:
        price = auction["starting_bid"]
        if price < auction["highest_bid_amount"]:
            price = auction["highest_bid_amount"]

        if "bin" in auction:
            item_id = item_utils.to_skyblock_item_id(auction["item_bytes"])
            if item_id not in bin_prices:
                bin_prices[item_id] = {"price": float("inf"), "sellers": 0}
            if bin_prices[item_id]["price"] > price:
                bin_prices[item_id] = {"price": price, "sellers": bin_prices[item_id]["sellers"] + 1}
        elif time.time() * 1000 + 60000 >= auction["end"]:
            item_id = item_utils.to_skyblock_item_id(auction["item_bytes"])
            if item_id not in auction_prices:
                auction_prices[item_id] = []
            auction_prices[item_id].append({"uuid": auction["uuid"], "price": price})

    return auction_prices, bin_prices


def auction_flip(budget):
    total_pages = requests.get("https://api.hypixel.net/skyblock/auctions?key=" + KEY).json()["totalPages"]
    urls = []
    for page in range(total_pages):
        urls.append("https://api.hypixel.net/skyblock/auctions?key=60b5fe52-8f17-432d-9f90-7fa79ae63ed5&&page=" +
                    str(page))

    datas = db.read_text(urls).map(json.loads).map(process_json).compute()
    bin_prices = {}
    for data in datas:
        _, new_bin_prices = data
        for key in new_bin_prices.keys():
            if key not in bin_prices.keys():
                bin_prices[key] = {"price": float("inf"), "sellers": 0}

            bin_prices[key]["sellers"] += new_bin_prices[key]["sellers"]
            if bin_prices[key]["price"] > new_bin_prices[key]["price"]:
                bin_prices[key]["price"] = new_bin_prices[key]["price"]
    best_flip = {}
    for data in datas:
        new_auction_prices, _ = data
        for key in new_auction_prices.keys():
            if key in bin_prices and bin_prices[key]["sellers"] >= AUCTION_ITEM_LIMIT:
                for auction in new_auction_prices[key]:
                    print(auction["price"], bin_prices[key]["price"])
                    if auction["price"] < budget:
                        profit = bin_prices[key]["price"] * 0.99 - auction["price"]
                        best_flip[(key, auction["uuid"], auction["price"],
                                   bin_prices[key]["price"])] = profit
    counter = collections.Counter(best_flip)

    return counter.most_common(15)
