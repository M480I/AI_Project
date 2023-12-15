from table import Table
from cell import Cell
from dfs import DFS
from bfs import BFS
from ucs import UCS


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
                if cell.location == 'T':
                    table.add_destination(cell)
            else:
                cell.init_weight = int(cell_inpt)

            table.cells[x][y] = cell
    
    table.add_successors()

    return table


def algorithm_result(name, algo) -> str:
    res = ("-" * 100 + "\n")
    res += name + "\n"
    res += f"{'Success' if algo.success else 'Failure'}\n"
    res += f"Path: {''.join(algo.final_path)}\n"
    res += f"Energy: {algo.final_energy}\n"
    res += f"Time: {algo.time}\n"
    return res


def do_search(table: Table, mode: tuple) -> str:

    res = ""

    if "all" in mode:
        mode = ("dfs", "bfs")

    if "dfs" in mode:
        res += algorithm_result("DFS", DFS(table))
    if "bfs" in mode:
        res += algorithm_result("BFS", BFS(table))

    res += ("-" * 100)

    return res
