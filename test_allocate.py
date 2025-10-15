from model import Batch, OrderLine, allocate, OutOfStock
from datetime import date, timedelta
import pytest


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch(
        "shipment-batch", "RETRO-CLOCK", 100, eta=date.today() + timedelta(days=1)
    )
    line = OrderLine("oreder-123", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "RETRO-CLOCK", 100, eta=date.today())
    medium = Batch(
        "normal-batch", "RETRO-CLOCK", 100, eta=date.today() + timedelta(days=1)
    )
    latest = Batch(
        "slow-batch", "RETRO-CLOCK", 100, eta=date.today() + timedelta(days=2)
    )
    line = OrderLine("oreder-123", "RETRO-CLOCK", 10)

    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_reference():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch(
        "shipment-batch", "RETRO-CLOCK", 100, eta=date.today() + timedelta(days=1)
    )
    line = OrderLine("oreder-123", "RETRO-CLOCK", 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch("batch1", "UNCOMFORTABLE-TABLE", 10, eta=date.today())
    # we allocate all the quantity
    allocate(OrderLine("oreder-123", "UNCOMFORTABLE-TABLE", 10), [batch])
    
    assert batch.available_quantity == 0
    
    # we try to allocate more than the available quantity and it should raise an exception
    with pytest.raises(OutOfStock, match="UNCOMFORTABLE-TABLE"):
        allocate(OrderLine("oreder-123", "UNCOMFORTABLE-TABLE", 1), [batch])
