import base64
import gzip
import io
from constants import *


def decode_nbt_to_string(string):
    return gzip.GzipFile(fileobj=io.BytesIO(base64.b64decode(string))).read().decode(
        "ISO-8859-1")


def to_custom_item_id(auction):
    nbt_string = decode_nbt_to_string(auction["item_bytes"])
    if "rarity_upgrades" in nbt_string:
        item_id = "RECOMBOBED "
    else:
        item_id = TIER_DISPLAY[auction["tier"]] + " "
    if "modifier" in nbt_string:
        item_id += auction["item_name"][auction["item_name"].find(" "):]
    else:
        if auction["item_name"].startswith("[Lvl "):
            pet_lvl = (int("".join(filter(str.isdigit, auction["item_name"][5:]))))
            if pet_lvl > 95:
                rounded = "95-100"
            elif pet_lvl > 90:
                rounded = "90-95"
            elif pet_lvl > 80:
                rounded = "80-90"
            elif pet_lvl > 70:
                rounded = "70-80"
            elif pet_lvl > 60:
                rounded = "60-70"
            elif pet_lvl > 45:
                rounded = "45-60"
            elif pet_lvl > 20:
                rounded = "20-45"
            else:
                rounded = "0-20"
            auction["item_name"] = auction["item_name"][:5] + str(rounded) + auction["item_name"][5+len(str(pet_lvl)):]
        item_id += auction["item_name"]
    return item_id


def to_skyblock_item_id(item_bytes):
    nbt_string = decode_nbt_to_string(item_bytes)
    item_id = ""

    field = ""
    i = len(nbt_string) - 1
    while True:
        if nbt_string[i] < ' ':
            if field == "di":
                break
            field = ""
        else:
            field += nbt_string[i]

        i -= 1
    i += 5
    c = nbt_string[i]
    while ord(c) >= 20:
        item_id += c
        i += 1
        c = nbt_string[i]
    return item_id
