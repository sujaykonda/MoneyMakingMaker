import base64
import collections
import gzip
import io

import dask.bag as db
import requests
import json
import time

from main import e

blacklist = {"ENCHANTED_BOOK", "PET", "RUNE", "NEW_YEAR_CAKE"}


def process_json(json_data):
    auction_prices = {}
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
                bin_prices[item_id] = [float("inf"), 0]
            if bin_prices[item_id][0] > price:
                bin_prices[item_id] = [price, bin_prices[item_id][0] + 1]

        if "bin" not in auction and item_id not in blacklist and time.time() * 1000 + 180000 > auction["end"]:
            if item_id not in auction_prices:
                auction_prices[item_id] = []
            auction_prices[item_id].append((auction["auctioneer"], price))

    return auction_prices, bin_prices


def auction_flip(budget, item_limit):
    total_pages = \
        requests.get("https://api.hypixel.net/skyblock/auctions?key=60b5fe52-8f17-432d-9f90-7fa79ae63ed5").json()[
            "totalPages"]
    urls = []
    for page in range(total_pages):
        urls.append(
            "https://api.hypixel.net/skyblock/auctions?key=60b5fe52-8f17-432d-9f90-7fa79ae63ed5&&page=" + str(page))

    datas = db.read_text(urls).map(json.loads).map(process_json).compute()
    bin_prices = {}
    for data in datas:
        _, new_bin_prices = data
        for key in new_bin_prices.keys():
            if key not in bin_prices.keys():
                bin_prices[key] = [float("inf"), 0]

            bin_prices[key][1] += new_bin_prices[key][1]
            if bin_prices[key][0] > new_bin_prices[key][0]:
                bin_prices[key][0] = new_bin_prices[key][0]
    best_flip = {}
    for data in datas:
        new_auction_prices, _ = data
        for key in new_auction_prices.keys():
            if key in bin_prices and bin_prices[key][1] >= item_limit:
                for i in range(len(new_auction_prices[key])):
                    if new_auction_prices[key][i][1] < budget:
                        profit = bin_prices[key][0] * 0.99 - new_auction_prices[key][i][1]
                        best_flip[(key, new_auction_prices[key][i][0], new_auction_prices[key][i][1], bin_prices[key][0], profit)] = profit
    counter = collections.Counter(best_flip)

    return counter.most_common(15)
