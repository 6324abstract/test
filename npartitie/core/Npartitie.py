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
                if cell.boundary_duplicated():
                    redundant_cells.append(cell)
        return redundant_cells


class Cell():
    def __init__(self, dimension: int, boundary: [Cell, ...], label: str = None, atomization: Union[Cell, None] = None):
        self.boundary = tuple(boundary)
        self.dimension = dimension
        self.atomization = atomization
        self.label = label

    def boundary_duplicated(self):  # check if a cell's boundary has redundancy O(d^3).
        for i in range(0, len(self.boundary) - 1):
            is_boundary = self.boundary[i + 1].has_boundary_helper(self.boundary[i])
            if is_boundary:
                return True
        return False

    def has_boundary(self, low_cell):
        '''
        :param low dimension cell
        :return: a list storing the result whether the low cell is connected to its boundaries
        '''
        if self.dimension == low_cell.dimension:
            return [self == low_cell]
        else:
            re = []
            for bnd in self.boundary:
                re.append(reduce(lambda x, y: x or y, bnd.has_boundary(low_cell)))
            return re

    def has_boundary_helper(self, low_cell):  # get the final result
        re_list = self.has_boundary(low_cell)
        return reduce(lambda x, y: x or y, re_list)


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
