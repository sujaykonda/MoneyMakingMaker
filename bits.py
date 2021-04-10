import base64
import collections
import gzip
import io

import dask.bag as db
import requests
import json

def coin_per_bits():
    bitcost = {
        "god potion": ["GOD_POTION", 1500],
        "kat flower": ["KAT_FLOWER", 500],
        "heat core": ["HEAT_CORE", 3000],
        "hyper catalyst upgrade": ["HYPER_CATALYST_UPGRADE", 300],
        "ultimate carrot candy upgrade": ["ULTIMATE_CARROT_CANDY_UPGRADE", 8000],
        "colossal exp bottle": ["COLOSSAL_EXP_BOTTLE_UPGRADE", 1200],
        "jumbo backpack upgrade": ["JUMBO_BACKPACK_UPGRADE", 4000],
        "minion storage expander": ["MINION_STORAGE_EXPANDER", 1500],
        "hologram": ["HOLOGRAM", 2000],
        "dungeon sack": ["LARGE_DUNGEON_SACK", 10000],
        "builders wand": ["BUILDERS_WAND", 12000],
        "block zapper": ["BLOCK_ZAPPER", 5000],
        "bits talisman": ["BITS_TALISMAN", 15000],
        "rune sack": ["RUNE_SACK", 10000],
        "autopets rule": ["AUTOPET_RULES_2", 21000],
        "kismet feather": ["KISMET_FEATHER", 1350],
        "speed enrichment": ["TALISMAN_ENRICHMENT_WALK_SPEED", 5000],
        "intelligence enrichment": ["TALISMAN_ENRICHMENT_INTELLIGENCE", 5000],
        "critical chance enrichment": ["TALISMAN_ENRICHMENT_CRITICAL_CHANCE", 5000],
        "critical damage enrichment": ["TALISMAN_ENRICHMENT_CRITICAL_DAMAGE", 5000],
        "strength enrichment": ["TALISMAN_ENRICHMENT_STRENGTH", 5000],
        "defense enrichment": ["TALISMAN_ENRICHMENT_DEFENSE", 5000],
        "health enrichment": ["TALISMAN_ENRICHMENT_HEALTH", 5000],
        "magic find enrichment": ["TALISMAN_ENRICHMENT_MAGIC_FIND", 5000],
        "ferocity enrichment": ["TALISMAN_ENRICHMENT_FEROCITY", 5000],
        "sea creature chance enrichment": ["TALISMAN_ENRICHMENT_SEA_CREATURE_CHANCE", 5000],
        "enrichment swapper": ["TALISMAN_ENRICHMENT_SWAPPER", 200],
    }