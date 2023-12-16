from cell import DirCell, bonus_map, Cell


class Table:

    def __init__(self, row_count, column_count) -> None:
        self.row_count = row_count
        self.column_count = column_count

        self.cells = [[None for _ in range(column_count)] for _ in range(row_count)]
        self.destinations: set[Cell] = set({})
        self.destinations_coords: set[tuple[int, int]] = set({})
        self.total_bonus = 0
        self.start = None


    def add_cell(self, x, y, cell) -> None:
        self.cells[x][y] = cell

        if cell.location is not None:
            self.total_bonus += bonus_map[cell.location]
            if cell.location == 'R':
               self.start = cell
    

    def add_destination(self, cell):
        self.destinations.add(cell)
        self.destinations_coords.add(cell.coordinates)


    def cell_of_coordinates(self, coordinates: tuple[int, int]):
        x, y = coordinates
        return self.cells[x][y]


    def add_successors(self):

        def is_valid(x, y) -> bool:

            if x >= self.row_count or y >= self.column_count or x < 0 or y < 0:
                return False
            return self.cells[x][y].is_open 


        diffs = [("U", (-1, 0)),
                 ("D", (1, 0)),
                 ("R", (0, 1)),
                 ("L", (0, -1)),
                 ]

        for x in range(self.row_count):
            for y in range(self.column_count):
                for d in diffs:
                    new_x, new_y = (x + d[1][0], y + d[1][1])
                    if is_valid(new_x, new_y):
                        self.cells[x][y].add_successor(
                            DirCell(d[0], self.cells[new_x][new_y])
                        )


    def reset(self):
        for x in range(self.row_count):
            for y in range(self.column_count):
                self.cells[x][y].reset()


    def __str__(self) -> str:
        res = ""
        for x in range(self.row_count):
            for y in range(self.column_count):
                space = 4 - len(self.cells[x][y].__str__())
                res += " " * (space // 2) + self.cells[x][y].__str__() + "  " * (space // 2) + "|"
            res += "\n" + "-" * (self.column_count * 6) + "\n"
        return res
