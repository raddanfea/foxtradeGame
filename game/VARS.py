from collections import defaultdict
from enum import Enum, auto

TYPES = {
    0: "weapon",
    1: "armor",
    2: "accessory",
    3: "other"
}

SPECIFIC_OBJECTS = {
    0: ["club", "dagger", "axe", "great axe", "mace", "spear", "hammer", "shortbow", "glaive", "halberd", "maul",
        "pike", "rapier", "scimitar", "whip", "crossbow", "set of arrows", "set of bolts", "staff"],
    1: ["light armor set", "mail armor set", "plate armor set", "breastplate armor", "half-plate armor",
        "knight armor set",
        "soldier armor set", "chain armor set", "ring armor set"],
    2: ["ring", "circlet", "crown", "set of earrings", "set of anklets", "bracelet"],
    3: ["alms box", "bell", "bedroll", "block of incense", "ordinary boots", "candle", "box of chalk",
        "bottle of ink", "ink pen", "stack of papers", "jug", "bag of trade goods", "box of trade goods",
        "ladder", "hooded lamp", "set of pitons", "pouch", "ordinary backpack", "sack", "set of clothes", "box of soap",
        "small knife", "bundle of torches", "vestments", "bundle of vials", "box of vials",
        "waterskin", "tinderbox", "set of tools"]
}

INTRODUCTIONS = ["This is ", "It is ", "You see ", "It's ", "You are shown ", "Before you is "]

RARITY = {
    0: "common",
    1: "uncommon",
    2: "rare",
    3: "exotic",
    4: "mythic"
}

MATERIAL = {
    0: ["wood", "stone", "iron", "leather", "copper", "brass", "lead", "bone", "hide"],
    1: ["steel", "cold iron", "bronze", "leather", "copper", "bronze", "ironwood", "bear-bone"],
    2: ["gold", "silver", "hardened steel", "leather", "copper", "bronze"],
    3: ["platinum", "mithril", "forged steel", "elven-wood"],
    4: ["obamanium", "adamantine", "dragon-bone", "orichalcum"],
}

COLOR = [
    "white", "silver", "golden", "brown", "green", "black", "skyblue", "ocean blue", "yellow", "pink", "amber", "cyan"
]

DECOR_DETAIL = {
    "writing": ["of a previous owner's emblem", "of a tragedy", "of a poem", "of a beautiful poem",
                "of an fairy tale", "of an unknown emblem"],
    "picture": ["of a tiger", "of a fallen noble's crest", "an unknown crest", "of a cock", "of a lion",
                "of a turtle", "of a dragon", "of a phoenix"],
    "jewelry": ["gem", "jewel"],
}

DECORATORS = {
    "writing": ["rune", "engraving"],
    "picture": ["engraving", "imprint", "flag"],
    "jewelry": ["studded", "embed"],
}

WORDS_IS = ["seems to be", "appears to be", "looks to be", "is"]
WORDS_WAS = ["seems to have been", "appears to have been", "looks to have been", "was"]
WORDS_COLORED = ["colored ", "tinted ", ""]

# NAME, PRICE, TYPE, ICON, DEFAULT AMOUNT
GENERIC_ITEMS = [
    ("Rations", 0.5, "Food", "bread", 10),
    ("Waterskin", 0.2, "Food", "bread", 10),
    ("Salt", 0.5, "Trade", "bread", 1),
    ("Spice", 2, "Trade", "bread", 1),
    ("Silverware", 5, "Trade", "bread", 1),
    ("Silk Bundle", 10, "Trade", "bread", 1),
    ("Gold Bar", 10, "Gold", "bread", 1),
]


TABULATOR = '        '
