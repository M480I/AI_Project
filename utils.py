from queue import PriorityQueue


def man_distance(cell_1, cell_2):
    x1, y1 = cell_1
    x2, y2 = cell_2
    return abs(x1 - x2) + abs(y1 - y2)


def cal_mst(nodes: list[tuple[int, int]]):

    # print("-" * 100)
    # print(nodes)

    def root(u):
        if par[u] == u:
            return u
        
        par[u] = root(par[u])
        return par[u]
    
    n = len(nodes)
    res = 0
    edges = PriorityQueue()
    mst_edges = []
    par = list(range(n))

    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if (i <= j):
                continue
            weight = man_distance(u, v)
            edges.put((weight, i, j))

    while not edges.empty():

        edge = edges.get()
        # print(edge, end=" ")
        weight, i, j = edge

        if root(i) != root(j):
            par[i] = root(j)
            res += weight
            mst_edges.append(edge)

    # print()
    # print(mst_edges, res)

    return res


nodes = [(2, 9), (5, 5), (3, 4)]
cal_mst(nodes)