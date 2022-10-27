from npartitie.core.Npartitie import Cell
def test_has_boundary():
    # construct a cwc with redundant
    cell_0_0 = Cell(0, [])
    cell_0_1 = Cell(0, [])
    cell_0_2 = Cell(0, [])

    cell_1_0 = Cell(1, [cell_0_0, cell_0_1])
    cell_1_1 = Cell(1, [cell_0_2, cell_0_1])
    cell_2_0 = Cell(2, [cell_1_1, cell_1_0])
    cell_2_1 = Cell(2, [cell_1_1])
    cell_3_0 = Cell(3, [cell_2_0])

    assert cell_3_0.has_boundary_helper(cell_2_0)
    assert cell_3_0.has_boundary_helper(cell_0_1)
    assert cell_2_1.has_boundary_helper(cell_0_2)
    assert not (cell_3_0.has_boundary_helper(cell_2_1))
    assert not (cell_2_1.has_boundary_helper(cell_0_0))
    assert not (cell_2_1.has_boundary_helper(cell_1_0))


def test_boundary_duplicated():
    cell_0_0 = Cell(0, [])
    cell_0_1 = Cell(0, [])
    cell_0_2 = Cell(0, [])

    cell_1_0 = Cell(1, [cell_0_0, cell_0_1])
    cell_1_1 = Cell(1, [cell_0_2, cell_0_1])
    cell_2_0 = Cell(2, [cell_0_0, cell_1_0])
    cell_2_1 = Cell(2, [cell_1_1])
    cell_3_0 = Cell(3, [cell_1_0, cell_2_1])

    assert cell_2_0.boundary_duplicated()
    assert not cell_3_0.boundary_duplicated()
