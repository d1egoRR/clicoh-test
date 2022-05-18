import pytest

from app.repositories.order import OrderRepository
from app.tests.factories import OrderFactory


@pytest.mark.django_db
def test_filter_by_id():
    order_id_not_existing = 1

    repository = OrderRepository()
    order = repository.filter_by_id(order_id_not_existing)

    assert order is None

    order_1 = OrderFactory()
    order_2 = OrderFactory()

    order = repository.filter_by_id(order_1.id)
    assert order == order_1

    order = repository.filter_by_id(order_2.id)
    assert order == order_2
