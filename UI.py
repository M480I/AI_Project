from table import Table
from cell import Cell
from dfs import DFS
from bfs import BFS
from ucs import UCS
from ids import IDS

import time


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


def algorithm_result(algo) -> str:
    res = ("-" * 100 + "\n")
    res += algo.title + "\n"
    res += f"{'Success' if algo.success else 'Failure'}\n"
    if algo.success:
        res += f"Path: {''.join(algo.final_path)}\n"
        res += f"Energy: {algo.final_energy}\n"
    res += f"Time: {algo.time}\n"
    return res


def do_search(table: Table, mode: tuple) -> str:

    res = ""

    if not len(mode):
        res = """
 ________________________
< Coding with kittens! >
 ------------------------
        \   /\_/\   /
         \\\\ ( o.o )//
          \\\\ > ^ < //
           \\\\_____//
           /       \\
          |  |   |  |
          |  |   |  |

"""

    if "all" in mode:
        mode = ("dfs", "bfs", "ucs", "ids")

    start_time = time.time()

    if "dfs" in mode:
        res += algorithm_result(DFS(table))
    if "bfs" in mode:
        res += algorithm_result(BFS(table))
    if "ucs" in mode:
        res += algorithm_result(UCS(table))
    if "ids" in mode:
        res += algorithm_result(IDS(table))

    res += ("-" * 100) + "\n"

    res += f"Total time: {time.time() - start_time}"

    return res
