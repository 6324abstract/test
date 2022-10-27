from __future__ import annotations
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

    def boundary_duplicated(self):  # check if a cell's boundary has redundancy.
        boundary_dict = {}
        for bnd in self.boundary:
            zero_boundaries = []
            while bnd.dimension > 0:
                zero_boundaries.append(bnd.boundary)  # reduce to  atomic cell
            for boundary in zero_boundaries:
                if boundary_dict.get(boundary) is not None:
                    return False
                else:
                    boundary_dict[boundary] = 0
        return True


    def reduction(self):
        '''
        #input boundary sorted by dimension
        #return 0 zero boundary
        '''
        if self.boundary is None:
            return []
        else:
            self.boundary=self.boundary[1:-1]
            return self.boundary.append(self.reduction())

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
    cell_0_0 = Cell(0, [],'00')
    cell_0_1 = Cell(0, [],'01')
    cell_0_2 = Cell(0, [],'02')

    cell_1_0 = Cell(1, [cell_0_0, cell_0_1],'10')
    cell_1_1 = Cell(1, [cell_0_1, cell_0_2],'11')
    cell_2_0 = Cell(2, [cell_1_0, cell_1_1],'20')
    cell_3_0 = Cell(3, [cell_2_0, cell_1_0],'21')

    print(cell_3_0.reduction())

