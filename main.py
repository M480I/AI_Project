from UI import input_table
from dfs import DFS
from bfs import BFS
from table import Table


table = input_table()

dfs = DFS(table)
print(dfs.success, "".join(dfs.final_path), dfs.energy, dfs.time)

print("-" * 100)

bfs = BFS(table)
print(bfs.succuss, "".join(bfs.path), bfs.final_energy, bfs.time)

print("-" * 100)

