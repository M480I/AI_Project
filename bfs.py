from table import Table
from cell import Cell, DirCell

import time
from queue import Queue
from decimal import Decimal


class BFS:
    
    def __init__(self, table: Table) -> None:
        
        self.table = table
        self.cell_of_index: list[tuple(int, int)] = []
        self.parent:list[int] = []
        self.pre_move:list[str] = []
        self.visited_dests:list[set[tuple(int, int)]] = []
        self.visited_bonuses: list[set[tuple(int, int)]] = []

        self.coords_count: list[set[tuple(int, int, int, int)]] = []
        self.visited_count: list[tuple(int, int)] = []

        self.energy:list[int] = []
        self.index = 0

        self.final_path = []
        self.success = False
        self.final_energy = None
        
        start_time = time.time()
        
        self.bfs()

        self.time = Decimal(time.time() - start_time)

        table.reset()


    def put_root(self) -> Queue:
        to_open = Queue()

        to_open.put(0)
        self.cell_of_index.append(self.table.cells[0][0].coordinates)
        self.parent.append(-1)
        self.pre_move.append("")
        self.visited_dests.append(set({}))
        self.visited_bonuses.append(set({}))
        self.coords_count.append({(0, 0, 0, 0)})
        self.visited_count.append((0, 0))
        self.energy.append(500 - self.table.cells[0][0].weight(False))

        return to_open
    

    def can_open(self, cell, parent) -> bool:

        eaten, visited_dest = self.visited_count[parent]

        if cell.location == 'T':
            if cell.coordinates in self.visited_dests[parent]:
                return False
        
        elif (*cell.coordinates, eaten, visited_dest) in self.coords_count[parent]:
            return False
        
        return True
    

    def has_bonus(self, cell, parent):
        if cell.coordinates in self.visited_bonuses[parent]:
            return False
        return True
    

    def update_visited_count(self, cell, parent):

        eaten, visited_dest = self.visited_count[parent]

        if cell.location == 'T':
            eaten += 1

        elif cell.location in ['I', 'C', 'B'] and self.has_bonus(cell, parent):
            visited_dest += 1

        self.visited_count.append((eaten, visited_dest))

        sett = self.coords_count[parent].copy()
        sett.add((*cell.coordinates, eaten, visited_dest))
        self.coords_count.append(sett)


    def update_dest_list(self, cell, parent):
        sett = self.visited_dests[parent].copy()
        if cell.location == 'T':
            sett.add(cell.coordinates)
        self.visited_dests.append(sett)


    def update_bonus_list(self, cell, parent):
        sett = self.visited_bonuses[parent].copy()
        if cell.location in ['I', 'C', 'visited_dest']:
            sett.add(cell.coordinates)
        self.visited_bonuses.append(sett)


    def is_search_done(self):
        if len(self.visited_dests[self.index]) == len(self.table.destinations):
            return True
        return False


    def find_path(self):
        parent = self.index
        while (self.parent[parent] != -1):
            self.final_path.append(self.pre_move[parent])
            parent = self.parent[parent]
        self.final_path.reverse()
    
    
    def bfs(self):
        
        to_open = self.put_root()

        while not to_open.empty():

            parent = to_open.get()
            cell = self.table.cell_of_coordinates(self.cell_of_index[parent])

            for next_cell in cell.successors:
                
                if not self.can_open(next_cell.cell, parent):
                    continue

                self.index += 1


                to_open.put(self.index)
                self.cell_of_index.append(next_cell.cell.coordinates)
                self.parent.append(parent)
                self.energy.append(self.energy[parent] - next_cell.cell.weight(self.has_bonus(next_cell.cell, parent)))
                self.pre_move.append(next_cell.direction)
                self.update_dest_list(next_cell.cell, parent)
                self.update_bonus_list(next_cell.cell, parent)
                self.update_visited_count(next_cell.cell, parent)


                if self.is_search_done():
                    self.success = True
                    self.final_energy = self.energy[self.index]
                    self.find_path()
                    break

            if self.success:
                break
