from table import Table
from cell import Cell, DirCell

import time
from queue import Queue


class BFS:
    
    def __init__(self, table: Table) -> None:
        
        self.table = table
        self.cell_of_index: list[tuple(int, int)] = []
        self.parent:list[int] = []
        self.pre_move:list[str] = []
        self.visited_dests:list[list[tuple(int, int)]] = []
        self.visited_bonuses: list[list[tuple(int, int)]] = []
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
        self.cell_of_index.append(self.table.cells[0][0].coordinate)
        self.parent.append(-1)
        self.energy.append(500 - self.table.cells[0][0].weight(False))
        self.pre_move.append("")
        self.visited_dests.append([])
        self.visited_bonuses.append([])

        return to_open
    

    def can_open(self, cell, parent) -> bool:
        if cell.coordinate in self.visited_dests[parent]:
            return False
        return True
    

    def has_bonus(self, cell, parent):
        if cell.coordinate in self.visited_bonuses[parent]:
            return False
        return True


    def update_dest_list(self, cell, parent):
        lst = self.visited_dests[parent].copy()
        if cell.location == 'T':
            lst.append(cell.coordinate)
        self.visited_dests.append(lst)


    def update_bonus_list(self, cell, parent):
        lst = self.visited_bonuses[parent].copy()
        if cell.location in ['I', 'C', 'B']:
            lst.append(cell.coordinate)
        self.visited_bonuses.append(lst)


    def is_search_done(self):
        if len(self.visited_dests[self.index]) == len(self.table.destinations):
            return True
        return False


    def find_path(self):
        u = self.index
        while (self.parent[u] != -1):
            self.path.append(self.pre_move[u])
            u = self.parent[u]
        self.path.reverse()
    
    
    def bfs(self):
        
        to_open = self.put_root()

        while not to_open.empty():

            u = to_open.get()
            cell = self.table.cell_of_coordinate(self.cell_of_index[u])

            for next_cell in cell.successors:
                
                if not self.can_open(next_cell.cell, u):
                    continue

                self.index += 1
                
                to_open.put(self.index)
                self.cell_of_index.append(next_cell.cell.coordinate)
                self.parent.append(u)
                self.energy.append(self.energy[u] - next_cell.cell.weight(self.has_bonus(next_cell.cell, u)))
                self.pre_move.append(next_cell.direction)
                self.update_dest_list(next_cell.cell, u)
                self.update_bonus_list(next_cell.cell, u)
                if self.is_search_done():
                    self.succuss = True
                    self.final_energy = self.energy[self.index]
                    self.find_path()
                    break

            if self.succuss:
                break
