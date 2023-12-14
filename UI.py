from table import Table
from cell import Cell


def input_table():

    row_count, column_count = map(int, input().split(" "))

    table = Table(row_count, column_count)

    for x in range(row_count):
        cells_inpt: str = input().split(" ")  

        for y, cell_inpt in enumerate(cells_inpt):

            cell = Cell(x, y)

            if cell_inpt == "X":
                cell.is_open = False
                table.cells[x][y] = cell
                continue
            
            cell.is_open = True

            if not cell_inpt[-1].isdigit():
                cell.location = cell_inpt[-1]
                cell.init_weight = int(cell_inpt[:-1])
            else:
                cell.init_weight = int(cell_inpt)

            table.cells[x][y] = cell
    
    table.add_successors()

    return table


