from model import Batch, OrderLine


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", 20, eta=None)
    line = OrderLine("order-123", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18
