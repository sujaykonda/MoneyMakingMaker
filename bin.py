import base64
import collections
import gzip
import io
import time

import dask.bag as db
import requests
import json

from main import e


blacklist = {"ENCHANTED_BOOK", "PET", "RUNE", "NEW_YEAR_CAKE", "CAKE_SOUL"}


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

        num_enchants = auction["extra"][len(auction["item_name"]):].split(" ")

        if "bin" in auction and item_id not in blacklist and not auction["claimed"] and time.time() * 1000 + 60000 < auction["end"]:
            if item_id not in bin_prices:
                bin_prices[item_id] = []
            bin_prices[item_id].append((auction["auctioneer"], price, num_enchants, auction["category"]))

    return bin_prices


def bin_flip(budget, profit_risk_factor):
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
        if len(bin_prices[key]) >= 2:
            selling_price = bin_prices[key][1][1]
            buying_price = bin_prices[key][0][1]
            profit = selling_price * 0.99 - buying_price
            if bin_prices[key][0][1] < budget and bin_prices[key][0][2] <= bin_prices[key][1][2] and profit > 20000:
                past_data = requests.get("https://api.slothpixel.me/api/skyblock/auctions/" + key + "?key=60b5fe52-8f17-432d-9f90-7fa79ae63ed5&&from=now-31d&&to=now-24d").json()
                sold = past_data["sold"]/7/24/60
                price = past_data["lowest_bin"]
                demand_at_selling_price = sold * (price**e[bin_prices[key][0][3]])/(selling_price**e[bin_prices[key][0][3]])
                best_flip[(key, bin_prices[key][0][0], bin_prices[key][0][1], bin_prices[key][1][1], profit, demand_at_selling_price)] = (demand_at_selling_price**profit_risk_factor) * profit

    counter = collections.Counter(best_flip)

    return counter.most_common(5)
