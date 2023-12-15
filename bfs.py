from table import Table
from cell import Cell, DirCell

import time
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
        self.visited_dest_count.append(0)

        return to_open
    

    def is_visited(self, cell, parent):
        x, y = cell.coordinates
        return self.visited[parent][x][y]
    

    def update_visited(self, cell, parent):
        x, y = cell.coordinates
        lst = self.visited[parent].copy()
        lst[x][y] = True
        self.visited.append(lst)
        if cell.location == 'T':
            self.visited_dest_count.append(self.visited_dest_count[parent] + 1)
        else:
            self.visited_dest_count.append(self.visited_dest_count[parent])


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

            u = to_open.get()
            cell = self.table.cell_of_coordinates(self.coord_of_index[u])

            for next_cell in cell.successors:
                
                if not self.can_open(next_cell.cell, u):
                    continue

                self.index += 1

                x, y = next_cell.cell.coordinates
                
                to_open.put(self.index)
                self.coord_of_index.append(next_cell.cell.coordinates)
                self.parent.append(u)
                self.energy.append(self.energy[u] - next_cell.cell.weight(self.visited[u][x][y]))
                self.pre_move.append(next_cell.direction)
                self.update_visited(next_cell.cell, u)
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
