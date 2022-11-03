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

    def boundary_duplicated(self):  # check if a cell's boundaries have redundancy.
        for i in range(0, len(self.boundary) - 1):  # assume boundary in order of dimension
            for j in range(i + 1, len(self.boundary)):
                is_boundary = self.boundary[j].is_connected_to(self.boundary[i])
                if is_boundary:
                    return True
        return False

    def get_connectivity_array(self, low_cell):
        '''
        :param low dimension cell to
        :return: a boolean array storing the low cell's connectedness to self.boundary and sub boundaries
        '''
        if self.dimension == low_cell.dimension:  # compare when same dimension
            return [self == low_cell]
        else:
            re = []
            for bnd in self.boundary:  #
                re.append(reduce(lambda x, y: x or y, bnd.get_connectivity_array(low_cell)))
            return re

    def is_connected_to(self, low_cell):  # high dimension cell's connection to low d cell
        re_list = self.get_connectivity_array(low_cell)
        return reduce(lambda x, y: x or y, re_list) # combine it by logic or


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
