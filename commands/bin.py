import collections
import time
import item_utils

import dask.bag as db
import requests
import json

import pandas as pd

from constants import *


def process_json(json_data):
    bin_prices = []
    auctions = json_data["auctions"]
    for auction in auctions:
        price = auction["starting_bid"]
        if price < auction["highest_bid_amount"]:
            price = auction["highest_bid_amount"]

        if "bin" in auction and not auction["claimed"] and time.time() * 1000 + 60000 < auction["end"]:
            item_id = item_utils.to_custom_item_id(auction)
            if not item_id.startswith("RECOMBOBED") and "✪" not in item_id:
                extra = len(auction["extra"][len(auction["item_name"]):].split(" "))
                auction_data = [
                    item_id,
                    auction["uuid"],
                    price,
                    extra,
                    json_data['page']
                    ]
                bin_prices.append(auction_data)

    return bin_prices


def bin_flip(budget):
    total_pages = requests.get("https://api.hypixel.net/skyblock/auctions?key=" + KEY).json()["totalPages"]
    urls = []
    for page in range(total_pages):
        urls.append("https://api.hypixel.net/skyblock/auctions?key=" + KEY + "&&page=" + str(page))

    datas = db.read_text(urls).map(json.loads).map(process_json).compute()
    all_data = []
    for d in datas:
        all_data = all_data + d

    prices_df = pd.DataFrame(all_data, columns=['item_id', 'uuid', 'price', 'extra', 'page']).sort_values(
        by=["item_id", "price"], ascending=True)
    prices_gb = prices_df.groupby('item_id')
    count_df = prices_gb.count()
    count_df = count_df[count_df["price"] > BIN_ITEM_LIMIT]
    flips_df = prices_gb.nth(0).join(prices_gb.nth(1), rsuffix="_next")
    flips_df = flips_df[flips_df["price"] < budget]
    flips_df = flips_df[flips_df["extra"] < flips_df["extra_next"]]
    flips_df = flips_df[flips_df.index.isin(count_df.index)]
    flips_df = flips_df.drop(columns=["extra", "extra_next", "page", "uuid_next", "page_next"])
    flips_df["profit"] = flips_df["price_next"] * 0.99 - flips_df["price"]
    flips_df = flips_df.sort_values("profit", ascending=False)

    return flips_df
