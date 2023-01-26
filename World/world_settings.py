from enum import IntEnum
from World.world_point import WorldPoint
from World.world import World

WORLD_SIZE = 500


class ElevationLabels(IntEnum):
    WATER = 0
    AVERAGE_HEIGHT = 1
    MOUNTAIN = 2


class HumidityLabels(IntEnum):
    ARID = 0
    AVERAGE_HUMDITY = 1
    WET = 2


class TemperatureLabels(IntEnum):
    COLD = 0
    AVERAGE_TEMPERATURE = 1
    HOT = 2


class LayerLabels(IntEnum):
    ELEVATION = 0
    HUMIDITY = 1
    TEMPERATURE = 2


class WorldSettings:
    def __init__(self):
        self.layers = {}
        self.add_layer(LayerLabels.ELEVATION, World())
        self.add_layer(LayerLabels.HUMIDITY, World())
        self.add_layer(LayerLabels.TEMPERATURE, World())
        self.humidity_thresholds = {}
        self.elevation_thresholds = {}
        self.temperature_thresholds = {}
        self.world_points = World()

    def set_humidity_threshold(self, label, value):
        if not isinstance(label, HumidityLabels):
            print("Wrong key passed")
            return
        if not isinstance(value, int) and not isinstance(value, float):
            print("Wrong value passed")
            return
        self.humidity_thresholds[label] = value

    def set_elevation_threshold(self, label, value):
        if not isinstance(label, ElevationLabels):
            print("Wrong key passed")
            return
        if not isinstance(value, int) and not isinstance(value, float):
            print("Wrong value passed")
            return
        self.elevation_thresholds[label] = value

    def set_temperature_threshold(self, label, value):
        if not isinstance(label, TemperatureLabels):
            print("Wrong key passed")
            return
        if not isinstance(value, int) and not isinstance(value, float):
            print("Wrong value passed")
            return
        self.temperature_thresholds[label] = value

    def add_world_point(self, point):
        if not isinstance(point, WorldPoint):
            print("Wrong value passed")
            return
        # self.world_points.append(WorldPoint)
        # set_point
        self.world_points.set_point(point.x, point.y)

    def get_humidity_percentage(self, label):
        return self.humidity_thresholds[label]

    def get_elevation_percentage(self, label):
        return self.elevation_thresholds[label]

    def get_temperature_percentage(self, label):
        return self.temperature_thresholds[label]

    def add_layer(self, layer_label, layer):
        if not isinstance(layer_label, LayerLabels):
            print("Wrong key passed")
            return
        if not isinstance(layer, World):
            print("Wrong value passed")
            return
        self.layers[layer_label] = layer

    def get_layer(self, layer_label):
        """
        Returns the layer specified
        :param layer_label: The label for the layer
        :return: A World object
        """
        return self.layers[layer_label]

    def set_value_from_layer_at(self, layer_label, x, y, value):
        if not isinstance(layer_label, LayerLabels):
            print("Wrong key passed")
            return
        if not isinstance(x, int) or not isinstance(y, int):
            print("Wrong coordinates passed")
            return

        self.layers[layer_label].set(x, y, value)

    def get_value_from_layer_at(self, layer_label, x, y):
        return self.layers[layer_label].get(x, y)
