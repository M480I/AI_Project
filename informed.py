from ucs import UCS
from utils import man_distance, cal_mst


class Greedy(UCS):

    def set_title(self):
        return "Greedy"


    def strong_h(self, index):

        cell = self.coords_of_index[index]

        max_possible_bonus = (self.table.total_bonus - self.total_bonus[index]) * (not self.is_search_done(index))

        unvisited_dests = self.table.destinations_coords.difference(self.visited_dests[index])
        dests: list[list[set[tuple[int, int]]]] = [[set({}) for _ in range(2)] for _ in range(2)]
        nodes = []
        

        for dest in unvisited_dests:

            x, y = cell

            x_dest, y_dest = dest
            x_comp = y_comp = None # x_comp determines if x_dest is lower(0) or greater/equal(1) than x

            if y_dest <= y and x_dest < x:
                x_comp = y_comp = 0

            elif y_dest < y and x_dest >= x:
                x_comp = 1
                y_comp = 0
            
            elif y_dest > y and x_dest <= x:
                x_comp = 0
                y_comp = 1
            
            elif y_dest >= y and x_dest > x:
                x_comp = y_comp = 1


            dests[x_comp][y_comp].add(dest)


        while len(nodes) < 4 and (dests[0][0] or dests[0][1] or dests[1][0] or dests[1][1]):
            for i in range(2):
                for j in range(2):

                    if not dests[i][j]:
                        continue

                    node = max(dests[i][j], key=lambda dest_cell : man_distance(dest_cell, cell))
                    dests[i][j].remove(node)
                    nodes.append(node)

                    if len(nodes) == 4:
                        break
                if len(nodes) == 4:
                    break

        nodes.append(cell)
        return max_possible_bonus - (cal_mst(nodes) * self.table.min_init_weight)
    

    def weak_h(self, index):

        cell = self.coords_of_index[index]

        max_possible_bonus = (self.table.total_bonus - self.total_bonus[index]) * (not self.is_search_done(index))

        unvisited_dests = self.table.destinations_coords.difference(self.visited_dests[index])
        
        farthest = max(unvisited_dests, key=lambda dest_cell : man_distance(cell, dest_cell))

        return max_possible_bonus - (man_distance(farthest, cell) * self.table.min_init_weight)  

    
    def weakest_h(self, index):  

        cell = self.coords_of_index[index]

        max_possible_bonus = (self.table.total_bonus - self.total_bonus[index]) * (not self.is_search_done(index))

        unvisited_dests = len(self.table.destinations) - len(self.visited_dests[index])
        
        return max_possible_bonus - (unvisited_dests * self.table.min_init_weight)
    

    def put_fringe(self, index):
        self.fringe.put((-self.strong_h(index), index))


class A_star(Greedy):

    def set_title(self):
        return "A*"
    
    def put_fringe(self, index):
        self.fringe.put((-(self.strong_h(index) + self.energy[index]), index))
