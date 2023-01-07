from poisson.point import PoissonPoint

class PoissonQueue:
    def __init__(self):
        self.queue = []

    def add_coord_to_queue(self, x, y):
        self.queue.append(PoissonPoint(x, y))

    def add_to_queue(self, obj):
        #print("item added")
        self.queue.append(obj)

    def get_next(self):
        #print("get next item")
        return self.queue[0]

    def pop_first(self):
        self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0
