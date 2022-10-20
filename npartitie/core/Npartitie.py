from __future__ import annotations
from typing import List, Tuple, Union
import networkx as nx


class CWcomplex():
    def __init__(self, layers: List[List[Cell]]):
        self.layers = layers


class Cell():
    def __init__(self, dimension: int, boundary: Tuple[Cell, ...], atomization: Union[Cell, None] = None):
        self.boundary = tuple(boundary)
        self.dimension = dimension
        self.atomization = atomization


def transfrom_CWc_to_npartite(c: CWcomplex):
    # for Li-san to implement
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
