from __future__ import annotations

from functools import reduce
from typing import List, Union
import networkx as nx


class CWcomplex():
    def __init__(self, layers: List[List[Cell]]):
        self.layers = layers

    def check_minimality(self):
        """
        # return list of cells for which minimality condition is not satisfied
        """
        redundant_cells = []
        for layer in self.layers:
            for cell in layer:
                if cell.has_duplicateboundary():
                    redundant_cells.append(cell)
        return redundant_cells


class Cell():
    def __init__(self, dimension: int, boundary: [Cell, ...], label: str = None, atomization: Union[Cell, None] = None):
        self.boundary = tuple(boundary)
        self.dimension = dimension
        self.atomization = atomization
        self.label = label

    def boundary_duplicated(self):  # check if a cell's boundary has redundancy O(d^3).
        for i in range(0,len(self.boundary)-1):
            is_boundary=self.boundary[i+1].has_boundary(self.boundary[i])[0][0]
            if is_boundary:
                return True
        return False

    def has_boundary(self, low_cell):  # time complexity=O(dimension^2)
        if self.dimension == low_cell.dimension:
            return [[self == low_cell]]
        else:
            for bnd in self.boundary:
                # map led to umlimited recrusion but seemed the same to me
                # return reduce(lambda x,y:x or y,map(self.has_boundary(low_cell),self.boundary))
                return [reduce(lambda x, y: x or y, bnd.has_boundary(low_cell))]

    def __str__(self):
        print(self.label)


def transfrom_CWc_to_npartite(c: CWcomplex):
    result = nx.MultiDiGraph()
    for layer in c.layers:
        layer_dimension = layer[0].dimension
        for cell in layer:
            result.add_node(cell, dimension=cell.dimension)
            if layer_dimension == 0:
                continue
            for bnd in cell.boundary:
                result.add_edge(cell, bnd)  # connect layer i to its boundary
            if layer_dimension >= 2 and cell.atomization is not None:  # check atomization
                result.add_edge(cell, cell.atomization)
    return result

if __name__=="__main__":
    cell_0_0 = Cell(0, [])
    cell_0_1 = Cell(0, [])
    cell_0_2 = Cell(0, [])

    cell_1_0 = Cell(1, [cell_0_0, cell_0_1])
    cell_1_1 = Cell(1, [cell_0_2, cell_0_1])
    cell_2_0 = Cell(2, [cell_1_1, cell_1_0])
    cell_2_1 = Cell(2, [cell_1_1])
    cell_3_0 = Cell(3, [cell_2_0])

    re= cell_3_0.has_boundary(cell_0_1)
    print(re)