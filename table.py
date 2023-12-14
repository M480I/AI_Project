from cell import Dir_cell


class Table:

    def __init__(self, row_count, column_count) -> None:
        self.row_count = row_count
        self.column_count = column_count
        self.cells = [[None for _ in range(column_count)] for _ in range(row_count)]


    def add_cell(self, x, y, cell) -> None:
        self.cells[x][y] = cell
    

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
                            Dir_cell(d[0], self.cells[new_x][new_y])
                        )


    def __str__(self) -> str:
        res = ""
        for x in range(self.row_count):
            for y in range(self.column_count):
                res += str(self.cells[x][y]) + " "
            res += "\n"
        return res
