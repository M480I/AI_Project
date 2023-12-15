from table import Table
from cell import Cell, DirCell

import time
import copy
from queue import Queue


class BFS:
    
    def __init__(self, table: Table) -> None:
        
        self.table = table
        self.coord_of_index: list[tuple(int, int)] = []
        self.parent:list[int] = []
        self.pre_move:list[str] = []
        self.visited:list[list[list[bool]]] = []
        self.visited_dest_count:list[int] = []
        self.energy:list[int] = []
        self.index = 0

        self.path = []
        self.succuss = False
        self.final_energy = None
        start_time = time.time()
        
        self.bfs()

        self.time = time.time() - start_time

        table.reset()


    def put_root(self) -> Queue:
        to_open = Queue()

        to_open.put(0)
        self.coord_of_index.append(self.table.cells[0][0].coordinates)
        self.parent.append(-1)
        self.energy.append(500 - self.table.cells[0][0].weight(False))
        self.pre_move.append("")
        self.visited.append([[False for _ in range(self.table.column_count)] for _ in range(self.table.row_count)])
        self.visited[0][0][0] = True
        self.visited_dest_count.append(0)

        return to_open
    

    def is_visited(self, cell, parent):
        x, y = cell.coordinates
        return self.visited[parent][x][y]
    

    def update_visited(self, cell, parent):
        x, y = cell.coordinates
        lst = copy.deepcopy((self.visited[parent]))
        lst[x][y] = True
        self.visited.append(lst)
        self.visited_dest_count.append(self.visited_dest_count[parent] + (cell.location == 'T'))


    def is_search_done(self):
        if self.visited_dest_count[self.index] == len(self.table.destinations):
            return True
        return False


    def find_path(self):
        u = self.index
        while (self.parent[u] != -1):
            self.path.append(self.pre_move[u])
            u = self.parent[u]
        self.path.reverse()


    def can_open(self, cell, parent):
        if cell.location != 'T':
            return True
        x, y = cell.coordinates
        if self.visited[parent][x][y]:
            return False
        return True
    
    
    def bfs(self):
        
        to_open = self.put_root()

        while not to_open.empty():

            parent = to_open.get()
            cell = self.table.cell_of_coordinates(self.coord_of_index[parent])

            for next_cell in cell.successors:
                
                if not self.can_open(next_cell.cell, parent):
                    continue

                self.index += 1

                x, y = next_cell.cell.coordinates
                
                to_open.put(self.index)
                self.coord_of_index.append(next_cell.cell.coordinates)
                self.parent.append(parent)
                self.energy.append(self.energy[parent] - next_cell.cell.weight(self.visited[parent][x][y]))
                self.pre_move.append(next_cell.direction)
                self.update_visited(next_cell.cell, parent)

                if self.is_search_done():
                    self.succuss = True
                    self.final_energy = self.energy[self.index]
                    self.find_path()
                    break

            if self.succuss:
                break


class UCS():

    def __init__(self, table: Table) -> None:

        self.table = table
        self.coord_of_index: list[tuple(int, int)]
