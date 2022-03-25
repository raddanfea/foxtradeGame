import random
from math import ceil
from time import sleep
from random import randint
from VARS import *


def get_aan(x: str):
    if x[0].capitalize() in ["A", "E", "I", "O", "U"]:
        return f'an {x}'
    else:
        return f'a {x}'


def getRandIntOfList(x):
    return randint(0, len(x) - 1)


def determineDecorations(rarity):
    sides = ["side", "middle", "upper part", "front"]
    out = ""
    if int(random.random()-0.2) or rarity:
        dectype = random.choice(list(DECORATORS))
        decdet = random.choice(DECOR_DETAIL[dectype])
        if int(random.random()):
            out = f'{get_aan(random.choice(COLOR)).capitalize()} ' \
                  f'{random.choice(DECORATORS[dectype])} {decdet} ' \
                  f'decorates its {random.choice(sides)}. '
        else:
            out = f'{get_aan(random.choice(MATERIAL[rarity])).capitalize()} ' \
                  f'{random.choice((DECORATORS[dectype]))} {decdet} ' \
                  f'decorates its {random.choice(sides)}. '

    return out


def determineAge(knowledge, age):
    year = "years"
    word_was = random.choice(WORDS_WAS)
    word_is = random.choice(WORDS_IS)

    if age == 1: year = "year"

    if age == 0:
        return f"It {word_is} brand new. "
    if knowledge == 0:
        if age < 10:
            return f"It {word_is} newish. "
        elif age > 100:
            return f"It {word_is} old. "
        else:
            return f"It {word_is} well used. "
    elif knowledge == 1:
        if age < 10:
            return f"It {word_was} made a few years ago. "
        elif age < 80:
            return f"It {word_was} made {round(age, -1)} {year} ago. "
        elif age < 700:
            return f"It {word_was} made {round(age, -2)} {year} ago. "
        else:
            return f"It {word_was} made {round(age, -3)} {year} ago. "
    elif knowledge == 2:
        if age < 10:
            return f"It {word_was} made {age} {year} ago. "
        elif age < 300:
            return f"It {word_was} made {round(age, -1)} {year} ago. "
        else:
            return f"It {word_was} made {round(age, -2)} {year} ago. "
    elif knowledge == 3:
        if age < 200:
            return f"It {word_was} made {age} {year} ago. "
        else:
            return f"It {word_was} made {round(age, -1)} {year} ago. "
    elif knowledge == 4:
        return f"It {word_was} made {age} {year} ago. "


def determineRarity(knowledge, rarity):
    knows = False
    if knowledge > rarity:
        knows = True
    elif int(random.random()):
        knows = True
    if knows:
        return f"The rarity {random.choice(WORDS_IS)} {RARITY[rarity]}. "
    else:
        return f"The rarity {random.choice(WORDS_IS)} at least {RARITY[knowledge + 1]}. "


def determineMaterial(rarity):
    base = f"The base material is {random.choice(MATERIAL[rarity])}"

    other = ""
    if rarity:
        other = f" with some parts of it made out of {random.choice(MATERIAL[rarity - 1])}"

    return f'{base}{other}. '


class SpecialItem:
    def __init__(self):
        self.type = getRandIntOfList(TYPES)
        self.quality = int(random.gammavariate(1, 1.5))
        self.rarity = self.genRarity()
        self.age = int(random.gammavariate(1, 2) * (self.rarity+1) ** 4)
        self.description = []

    def getType(self):
        return self.type

    def getAge(self):
        return self.age

    def getFields(self):
        return f'TYPE:{TYPES[self.type].capitalize()} ' \
               f'AGE:{self.age} ' \
               f'QUALITY:{self.quality} ' \
               f'RARITY:{RARITY[self.rarity]} ' \
               f'VALUE:{self.getGoldValue()} '

    def genDescription(self, knowledge=0):
        description = f'{random.choice(INTRODUCTIONS)}' \
                      f'{get_aan(random.choice(COLOR))} {random.choice(WORDS_COLORED)}' \
                      f'{random.choice(SPECIFIC_OBJECTS[self.type])}. '
        lines = []
        lines.append(determineRarity(knowledge, self.rarity))
        lines.append(determineMaterial(self.rarity))
        lines.append(determineDecorations(self.rarity))
        lines.append(determineAge(knowledge, self.age))
        self.description = [description].append(lines)

        return f'{description}{"".join(lines)}'

    def getGoldValue(self, shortages: list = []):
        value = 10
        value += self.quality * 100
        if self.age > 10:
            value += self.age * 1.3 ** 1.1
        if self.type in shortages:
            value = value ** 1.3
        value *= float(f'1.{self.quality}')
        return int(value)

    def genRarity(self):
        x = int(random.gammavariate(2, 125) / 200)
        if x > 4: x = 4
        self.quality += x
        return x


if __name__ == '__main__':
    for _ in range(5):
        x = SpecialItem()
        print(x.genDescription())
