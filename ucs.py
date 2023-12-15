from bfs import BFS

from queue import PriorityQueue


class UCS(BFS):

    def set_title(self):
        return "UCS"


    def init_fringe(self):
        return PriorityQueue()
    

    def put_fringe(self, index):
        self.fringe.put((-self.energy[index], index))
    

    def get_fringe(self):
        return self.fringe.get()[1]
    