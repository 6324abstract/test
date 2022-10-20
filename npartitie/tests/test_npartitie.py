import pytest
import networkx as nx
from  npartitie.core.Npartitie import *


def test_empty_complex():
    empty_complex = CWcomplex([])
    nc = transfrom_CWc_to_npartite(empty_complex)
    assert len(nc) == 0
    assert nc.size() == 0


def test_atomic_links():
    # construct cwc with atomic links
    cell_0_0 = Cell(0, [])
    cell_0_1 = Cell(0, [])
    cell_1_0 = Cell(1, [cell_0_0, cell_0_1])
    cell_2_0 = Cell(2, [cell_1_0])

    c = CWcomplex([[cell_0_0, cell_0_1], [cell_1_0], [cell_2_0]])
    nc = transfrom_CWc_to_npartite(c)

    # check atomic link presence and orientation simultaneously as digraph
    assert nc.has_edge(cell_1_0, cell_0_0)
    assert nc.has_edge(cell_1_0, cell_0_1)
    assert nc.has_edge(cell_2_0, cell_1_0)


def test_big_complex():  # generate a different cwc with test_atomic_links for diversity?
    # construct cwc with atomic links
    cell_0_0 = Cell(0, [])
    cell_0_1 = Cell(0, [])
    cell_0_2 = Cell(0, [])

    cell_1_0 = Cell(1, [cell_0_0, cell_0_1])
    cell_1_1 = Cell(1, [cell_0_1, cell_0_2])
    cell_1_2 = Cell(1, [cell_0_2, cell_0_0])
    cell_2_0 = Cell(2, [cell_1_0, cell_1_1])
    cell_3_0 = Cell(3, [cell_2_0])

    c = CWcomplex([[cell_0_0, cell_0_1, cell_0_2], [cell_1_0, cell_1_1, cell_1_2], [cell_2_0], [cell_3_0]])
    nc = transfrom_CWc_to_npartite(c)

    # construct expected graph by hand
    expected_npartite = nx.MultiDiGraph()
    # initialize nodes(cell)

    np_nodes = [
        cell_0_0,
        cell_0_1,
        cell_0_2,
        cell_1_0,
        cell_1_1,
        cell_1_2,
        cell_2_0,
        cell_3_0
    ]
    # initialize edges
    np_edges = [
        (cell_1_0, cell_0_0),
        (cell_1_0, cell_0_1),
        (cell_1_1, cell_0_1),
        (cell_1_1, cell_0_2),
        (cell_1_2, cell_0_2),
        (cell_1_2, cell_0_0),
        (cell_2_0, cell_1_1),
        (cell_2_0, cell_1_2),
        (cell_3_0, cell_2_0)
    ]

    expected_npartite.add_nodes_from(np_nodes)
    expected_npartite.add_edges_from(np_edges)

    assert nx.is_isomorphic(nc, expected_npartite)
