import collections

import requests
from constants import *


def farming_level_eq(level):
    return (level * 4 + 100) if (level <= 50) else ((level - 50) * 4 + 300)


def farming(farming_level):
    fly_speed = 10.92
    sprint_speed = 5.612
    ladder_speed = 2.5
    crop_settings = {
        "Pumpkin (Two Row)":      ["ENCHANTED_PUMPKIN",       160,       sprint_speed, 300, 2, 1.35, 25],
        "Sugarcane (Two Row)":    ["ENCHANTED_SUGAR",         160,       sprint_speed, 260, 4, 1,    261],
        "Melon (Two Row)":        ["ENCHANTED_MELON",         160,       sprint_speed, 300, 2, 6.6,  25],
        "Carrot (Fly)":           ["ENCHANTED_GOLDEN_CARROT", 160 * 128, fly_speed,    100, 3, 4.5,  261],
        "Potato (Fly)":           ["HOT_POTATO_BOOK",         160 * 160, fly_speed,    100, 3, 4.5,  261],
        "Nether Wart (Fly)":      ["ENCHANTED_NETHER_STALK",  160,       fly_speed,    100, 3, 3,    261],
        "Cocoa Beans (Fly)":      ["ENCHANTED_COCOA",         160,       fly_speed,    100, 3, 1,    25],
        "Cocoa Beans (Semi Afk)": ["ENCHANTED_COCOA",         160,       ladder_speed, 100, 4, 1,    25],
    }
    bazaar_data = requests.get("https://api.hypixel.net/skyblock/bazaar?key=" + KEY).json()["products"]
    farming_profits = {}
    for crop in crop_settings.keys():
        profit_per_item = bazaar_data[crop_settings[crop][0]]["sell_summary"][0]["pricePerUnit"] / crop_settings[crop][1]
        items_per_second = crop_settings[crop][2] * crop_settings[crop][3]/100 * crop_settings[crop][4] * crop_settings[crop][5]
        farming_fortune = farming_level_eq(farming_level) + crop_settings[crop][6]
        profit_per_hour = items_per_second * profit_per_item * farming_fortune/100 * 3600
        farming_profits[crop] = profit_per_hour

    return farming_profits
