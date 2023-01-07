from World.world_point import WorldPoint

WORLD_SIZE = 500


class World:
    def __init__(self):
        self.grid = {}

        for x in range(WORLD_SIZE):
            for y in range(WORLD_SIZE):
                self.add_new_world_value(x, y)

    def get(self, x, y):
        return self.grid[x, y]

    def set(self, x, y, point):
        if isinstance(point, WorldPoint):
            self.grid[x, y] = point

    def add_new_world_value(self, x, y):
        self.grid[x, y] = WorldPoint()

    def get_origin_coordinates(self):
        return [
            int(len(self.grid)/2),
            int(len(self.grid)/2)
        ]

    def is_point(self, x, y):
        b = True
        #try:
        b = self.grid[x, y].is_point
        #except Exception:
        #    b = True
        #    pass
        return b

    def set_point(self, x, y):
        self.grid[x, y].is_point = True
