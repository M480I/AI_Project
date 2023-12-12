class Cell:

    def __init__(self, x, y, is_open = None, weight = None, location = None) -> None:
        self.x = x
        self.y = y
        self.is_open = is_open
        self.location = location
        self.weight = weight
        self.successors: list[dict] = []


    def add_successor(self, *other: list[dict]):
        self.successors.append(other)

    
    def __str__(self):
        if not self.is_open:
            return "X"
        return str(self.weight) + ("" if self.location is None else self.location)
    