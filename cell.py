bonus_map = {"C": 10,
             "B": 5,
             "I": 12,
             "R": 0,
             "T": 0,
             }


class DirCell:
    
    def __init__(self, direction, cell) -> None:
        self.cell = cell
        self.direction = direction


    def __str__(self) -> str:
        return f"{self.cell.__str__()} in {self.direction}"


class Cell:

    def __init__(self, x, y, is_open = None, init_weight = None, location = None) -> None:
        self.x = x
        self.y = y
        self.is_open = is_open
        self.init_weight = init_weight
        self.location = location
        
        self.successors: list[dict] = []

        self.mark = False
        self.eaten_count = 0
        self.visited_dest_count = 0


    def add_successor(self, *other: list[DirCell]):
        self.successors.append(*other)


    def weight(self, has_bonus):
        bonus = 0 if self.location is None else bonus_map[self.location] 
        return self.init_weight - (has_bonus) * bonus
    

    def reset(self):
        self.mark = False
        self.eaten_count = 0
        self.visited_dest_count = 0

    
    @property
    def coordinates(self):
        return (self.x, self.y)

    
    def __str__(self):
        if not self.is_open:
            return "X"
        return f"{self.init_weight}{'' if self.location is None else self.location}"
    