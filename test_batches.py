import pytest
from model import Batch, OrderLine


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=None),
        OrderLine("order-123", sku, line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line("SMALL-TABLE", 20, 2)

    batch.allocate(line)

    assert batch.available_quantity == 18


# ================================


@pytest.mark.parametrize(
    "batch_qty, line_qty, expected",
    [
        (20, 2, True),  # available > required
        (2, 20, False),  # available < required
        (2, 2, True),  # available == required
    ],
)
def test_can_allocate(batch_qty, line_qty, expected):
    batch, line = make_batch_and_line("SMALL-TABLE", batch_qty, line_qty)
    assert batch.can_allocate(line) is expected


def test_cannot_allocate_if_sku_does_not_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-TABLE", 100, eta=None)
    different_sku_line = OrderLine("order-123", "ANOTHER-TABLE", 10)
    assert batch.can_allocate(different_sku_line) is False

