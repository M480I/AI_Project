from table import Table
from cell import Cell, DirCell

import time


class DFS:
    
    def __init__(self, table: Table) -> None:

        self.title = self.set_title()
        self.table = table
        self.success = False
        self.limit = None
        self.max_height = 0

        self.do_search()


    def set_title(self):
        return "DFS"
    

    def init_search(self):

        self.final_energy = 500 - self.table.cells[0][0].weight(0)
        self.final_path = []
        self.eaten_count = 0
        self.visited_dest_count = 0
        self.table.cells[0][0].mark = True
        self.height = 0

    
    def do_search(self):

        self.init_search()

        start_time = time.time()

        self.dfs(self.table.cells[0][0])

        self.time = (time.time() - start_time)

        self.table.reset()


    def can_open(self, cell) -> bool:

        if (self.limit is not None) and (self.limit < self.height):
            return False

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
            return
        
        
        for next_cell in cell.successors:

            if not self.can_open(next_cell.cell):
                continue

            pre_eaten_count = next_cell.cell.eaten_count
            pre_visited_dest_count = next_cell.cell.visited_dest_count
            next_cell.cell.eaten_count = self.eaten_count
            next_cell.cell.visited_dest_count = self.visited_dest_count
            self.update_visited(next_cell.cell, 1)
            self.final_path.append(next_cell.direction) 
            self.final_energy -= next_cell.cell.weight(not next_cell.cell.mark)
            pre_mark = next_cell.cell.mark
            next_cell.cell.mark = True
            self.height += 1
            self.max_height = max(self.max_height, self.height)

            self.dfs(next_cell.cell)

            if self.success:
                return
            
            self.height -= 1
            next_cell.cell.mark = pre_mark
            self.final_energy += next_cell.cell.weight(not next_cell.cell.mark)
            self.final_path.pop()
            self.update_visited(next_cell.cell, -1)
            next_cell.cell.eaten_count = pre_eaten_count
            next_cell.cell.visited_dest_count = pre_visited_dest_count
