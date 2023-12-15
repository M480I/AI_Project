from table import Table
from cell import Cell, DirCell

import time


class DFS:
    
    def __init__(self, table: Table) -> None:
        
        self.table = table

        self.success = False
        self.final_energy = 500 - table.cells[0][0].weight(0)
        self.path = []
        self.final_path = []

        self.eaten_count = 0
        self.visited_dest_count = 0

        start_time = time.time()
        table.cells[0][0].mark = True

        self.dfs(table.cells[0][0])

        self.time = (time.time() - start_time)

        table.reset()


    def can_open(self, cell) -> bool:

        if not cell.mark:
            return True
        
        if cell.location == 'T':
            return False
        
        if self.eaten_count == cell.eaten_count and self.visited_dest_count == cell.visited_dest_count:
            return False
        
        return True
    

    def update_visited(self, new_cell, value):

        if new_cell.location == 'T' and not new_cell.mark:
            self.visited_dest_count += value
        
        elif new_cell.location in ['C', 'I', 'B'] and not new_cell.mark:
            self.eaten_count += value
            

    def is_search_done(self) -> bool:
        for dest in self.table.destinations:
            if not dest.mark:
                return False
        return True
    
    
    def dfs(self, cell):

        if self.is_search_done():
            self.success = True
            self.final_path = self.path.copy()
            return
        
        
        for next_cell in cell.successors:

            if not self.can_open(next_cell.cell):
                continue

            pre_eaten_count = next_cell.cell.eaten_count
            pre_visited_dest_count = next_cell.cell.visited_dest_count
            next_cell.cell.eaten_count = self.eaten_count
            next_cell.cell.visited_dest_count = self.visited_dest_count
            self.update_visited(next_cell.cell, 1)
            self.path.append(next_cell.direction) 
            self.final_energy -= next_cell.cell.weight(not next_cell.cell.mark)
            pre_mark = next_cell.cell.mark
            next_cell.cell.mark = True

            self.dfs(next_cell.cell)

            if self.success:
                return
            
            next_cell.cell.mark = pre_mark
            self.final_energy += next_cell.cell.weight(not next_cell.cell.mark)
            self.path.pop()
            self.update_visited(next_cell.cell, -1)
            next_cell.cell.eaten_count = pre_eaten_count
            next_cell.cell.visited_dest_count = pre_visited_dest_count
