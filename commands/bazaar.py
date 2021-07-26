import collections

import requests
from constants import *


def bazaar_flip(budget):
    bazaar_data = requests.get("https://api.hypixel.net/skyblock/bazaar?key=60b5fe52" + KEY).json()["products"]
    profits = {}
    for product_id in bazaar_data.keys():
        if len(bazaar_data[product_id]["sell_summary"]) > 0 and len(bazaar_data[product_id]["buy_summary"]) > 0:
            buy_price = bazaar_data[product_id]["sell_summary"][0]["pricePerUnit"]
            sell_price = bazaar_data[product_id]["buy_summary"][0]["pricePerUnit"]

            margin = sell_price * 0.9875 - buy_price
            demand = bazaar_data[product_id]["quick_status"]["sellMovingWeek"]/7/24/60
            demand *= (buy_price**0.3)/(sell_price**0.3)
            profit_per_min = margin * demand
            profits[(product_id, buy_price, sell_price, demand)] = profit_per_min

    counter = collections.Counter(profits)

    return counter.most_common(10)

