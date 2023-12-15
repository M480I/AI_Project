from dfs import DFS

import time


class IDS(DFS):
    
    def set_title(self):
        return "IDS"
    

    def do_search(self):

        start_time = time.time()

        i = 0
        max_height = None
        while not self.success:
            self.init_search()
            self.limit = i
            self.dfs(self.table.cells[0][0])
            self.table.reset()
            if max_height == self.max_height:
                break
            max_height = self.max_height
            i += 1

        self.time = (time.time() - start_time)

