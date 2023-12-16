from ucs import UCS


class Greedy(UCS):

    def heuristic(self, index):
        possible_bonus = self.table.total_bonus - self.total_bonus

        unvisited_dests = self.table.destinations_coords.difference(self.visited_dests)
        dests: list[list[set[tuple[int, int]]]] = [[set({}) for _ in range(3)] for _ in range(3)]
        
        x, y = self.coords_of_index(index)

        for dest in unvisited_dests:
            x_dest, y_dest = dest

            pass
