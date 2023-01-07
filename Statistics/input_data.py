from enum import IntEnum
from logging import debug
keys_percentages = [
    "water",
    "beach",
    "plains",
    "mountain",
    "desert"
]


class PercentageKeys(IntEnum):
    WATER = 0
    BEACH = 1
    PLAINS = 2
    MOUNTAIN = 3
    DESERT = 4



class InputData:
    def __init__(self):
        self.percentages = {}
        self.age = 0

    def add_percentage(self, enum_key, value):
        self.percentages[keys_percentages[enum_key]] = int(value)

    def set_age(self, value):
        self.age = int(value)

    def get_water_percentage(self):
        return self.percentages[keys_percentages[PercentageKeys.WATER]]

    def get_beach_percentage(self):
        return self.get_water_percentage() \
               + self.percentages[keys_percentages[PercentageKeys.BEACH]]

    def get_plain_percentage(self):
        return self.get_beach_percentage() \
               + self.percentages[keys_percentages[PercentageKeys.PLAINS]]

    def get_mountain_percentage(self):
        return 100
