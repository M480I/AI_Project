from table import Table
from cell import Cell, DirCell, bonus_map

import time
from queue import Queue


class BFS:
    
    def __init__(self, table: Table) -> None:
        
        self.title = self.set_title()
        self.table = table

        self.coords_of_index: list[tuple[int, int]] = []
        self.parent:list[int] = []
        self.pre_move:list[str] = []
        
        self.visited_dests:list[set[tuple[int, int]]] = []
        self.visited_bonuses: list[set[tuple[int, int]]] = []

        self.coords_count: list[set[tuple[int, int, int, int]]] = []
        self.visited_count: list[tuple[int, int]] = []

        self.energy:list[int] = []
        self.total_bonus:list[int] = []
        self.index = 0
        self.fringe = self.init_fringe()

        self.final_path = []
        self.success = False
        self.final_energy = None
        
        start_time = time.time()
        
        self.search()

        self.time = time.time() - start_time

        table.reset()

    
    def set_title(self):
        return "BFS"


    def init_fringe(self):
        return Queue()    
    

    def put_fringe(self, index):
        self.fringe.put(index)


    def get_fringe(self):
        return self.fringe.get()


    def put_root(self) -> None:
        
        x, y = self.table.start.coordinates
        self.energy.append(500 - self.table.start.weight(False))
        self.total_bonus.append(0)
        self.coords_of_index.append(self.table.start.coordinates)
        self.parent.append(-1)
        self.pre_move.append("")
        self.visited_dests.append(set({}))
        self.visited_bonuses.append(set({}))
        self.coords_count.append({(x, y, 0, 0)})
        self.visited_count.append((0, 0))
        self.put_fringe(0)
    

    def can_open(self, cell, parent) -> bool:

        eaten, visited_dest = self.visited_count[parent]

        if cell.location == 'T' and cell.coordinates in self.visited_dests[parent]:
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
        if cell.location in ['I', 'C', 'B']:
            sett.add(cell.coordinates)
        self.visited_bonuses.append(sett)


    def is_search_done(self, index):
        return len(self.visited_dests[index]) == len(self.table.destinations)


    def find_path(self, index):
        parent = index
        while (self.parent[parent] != -1):
            self.final_path.append(self.pre_move[parent])
            parent = self.parent[parent]
        self.final_path.reverse()
    
    
    def search(self):
        
        self.put_root()

        while not self.fringe.empty():

            parent = self.get_fringe()
            cell = self.table.cell_of_coordinates(self.coords_of_index[parent])

            if self.is_search_done(parent):
                self.success = True
                self.final_energy = self.energy[parent]
                self.find_path(parent)
                break
        
            for next_cell in cell.successors:
                
                if not self.can_open(next_cell.cell, parent):
                    continue

                self.index += 1


                self.energy.append(self.energy[parent] - next_cell.cell.weight(self.has_bonus(next_cell.cell, parent)))
                if next_cell.cell.location is not None and self.has_bonus(next_cell.cell, parent):
                    self.total_bonus.append(bonus_map[next_cell.cell.location] + self.total_bonus[parent])
                else:
                    self.total_bonus.append(self.total_bonus[parent])
                self.coords_of_index.append(next_cell.cell.coordinates)
                self.parent.append(parent)
                self.pre_move.append(next_cell.direction)
                self.update_dest_list(next_cell.cell, parent)
                self.update_bonus_list(next_cell.cell, parent)
                self.update_visited_count(next_cell.cell, parent)
                self.put_fringe(self.index)

                if self.title == "BFS" and self.is_search_done(self.index):
                    self.success = True
                    self.final_energy = self.energy[self.index]
                    self.find_path(self.index)
                    break
            
            if self.success:
                break