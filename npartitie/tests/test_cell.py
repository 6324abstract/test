from npartitie.core.Npartitie import Cell


def test_is_connected():
    # construct a cwc with redundant
    cell_0_0 = Cell(0, [])
    cell_0_1 = Cell(0, [])
    cell_0_2 = Cell(0, [])

    cell_1_0 = Cell(1, [cell_0_0, cell_0_1])
    cell_1_1 = Cell(1, [cell_0_2, cell_0_1])
    cell_2_0 = Cell(2, [cell_1_1, cell_1_0])
    cell_2_1 = Cell(2, [cell_1_1])
    cell_3_0 = Cell(3, [cell_2_0])

    # check connectivity
    assert cell_3_0.is_connected_to(cell_3_0)  # trivial case:identical
    assert cell_3_0.is_connected_to(cell_2_0)  # trivial  case: direct connected
    assert cell_3_0.is_connected_to(cell_0_1)  # indirect: in subset
    # check disconncetivity
    assert not (cell_3_0.is_connected_to(cell_2_1))  # trivial case:
    assert not (cell_2_1.is_connected_to(cell_0_0))  # indirect connected

def test_boundary_duplicated():
    cell_0_0 = Cell(0, [])
    cell_0_1 = Cell(0, [])
    cell_0_2 = Cell(0, [])

    cell_1_0 = Cell(1, [cell_0_0, cell_0_1])
    cell_1_1 = Cell(1, [cell_0_2, cell_0_1])
    cell_2_0 = Cell(2, [cell_0_0, cell_1_0])
    cell_2_1 = Cell(2, [cell_0_0, cell_1_1])
    cell_3_0 = Cell(3, [cell_0_1, cell_2_1])

    assert cell_2_0.boundary_duplicated()
    assert not cell_2_1.boundary_duplicated()
    assert cell_3_0.boundary_duplicated()


def test_with_illustration():
    """
    .. image:: img/test_with_illustration.png
        :alt: code_quality
    """
    # TODO: implement test
    # TODO: change test name to smth meaningful
    # TODO (optional): add description
