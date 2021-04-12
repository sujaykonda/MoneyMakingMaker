import collections

import requests
from main import e


def bazaar_flip(budget):
    bazaar_data = requests.get("https://api.slothpixel.me/api/skyblock/bazaar/").json()
    profits = {}
    for product_id in bazaar_data.keys():
        if len(bazaar_data[product_id]["sell_summary"]) > 0 and len(bazaar_data[product_id]["buy_summary"]) > 0:
            buy_price = bazaar_data[product_id]["sell_summary"][0]["pricePerUnit"]
            sell_price = bazaar_data[product_id]["buy_summary"][0]["pricePerUnit"]

            margin = sell_price - buy_price
            demand = bazaar_data[product_id]["quick_status"]["sellMovingWeek"]/7/24/60
            demand *= (buy_price**e["bazaar"])/(sell_price**e["bazaar"])
            #demand /= (margin/buy_price + 1)**0.7
            profit_per_min = margin * demand
            profits[product_id] = profit_per_min

    counter = collections.Counter(profits)

    return counter.most_common(10)

