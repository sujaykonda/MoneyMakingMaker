import base64
import collections
import gzip
import io

import dask.bag as db
import requests
import json


blacklist = {"ENCHANTED_BOOK", "PET", "RUNE", "NEW_YEAR_CAKE"}


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

        if "bin" in auction and item_id not in blacklist:
            if item_id not in bin_prices:
                bin_prices[item_id] = []
            bin_prices[item_id].append((auction["auctioneer"], price))

    return bin_prices


def bin_flip(budget, item_limit):
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
        for key in data.keys():
            if key not in bin_prices.keys():
                bin_prices[key] = []
            bin_prices[key] += data[key]
    best_flip = {}
    for key in bin_prices.keys():
        bin_prices[key] = sorted(bin_prices[key], key=lambda row: row[1])
        if len(bin_prices[key]) >= item_limit and bin_prices[key][0][1] < budget:
            sold = 1
            profit = bin_prices[key][1][1] - bin_prices[key][0][1] * 0.99
            best_flip[(key, bin_prices[key][0][0], profit)] = profit * sold**0.05

    counter = collections.Counter(best_flip)

    return counter.most_common(5)
