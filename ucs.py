from table import Table
from cell import *

import time
import heapq


class UCS():

    def __init__(self, table: Table) -> None:

        self.table = table
        self.coord_of_index: list[tuple(int, int)]