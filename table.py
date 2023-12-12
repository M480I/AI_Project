class Table:


    def __init__(self, row_count, column_count) -> None:
        self.row_count = row_count
        self.column_count = column_count
        self.cells = [[None for _ in range(column_count)] for _ in range(row_count)]

    def add_cell(self, x, y, cell) -> None:
        self.cells[x][y] = cell
    

    def __str__(self) -> str:
        res = ""
        for x in range(self.row_count):
            for y in range(self.column_count):
                res += str(self.cells[x][y]) + " "
            res += "\n"
        return res
    

