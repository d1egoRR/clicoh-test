import pytest

from app.repositories.order_detail import OrderDetailRepository
from app.tests.factories import OrderDetailFactory


@pytest.mark.django_db
def test_filter_by_id():
    order_detail_id_not_existing = 1

    repository = OrderDetailRepository()
    order_detail = repository.filter_by_id(order_detail_id_not_existing)

    assert order_detail is None

    order_detail_1 = OrderDetailFactory()
    order_detail_2 = OrderDetailFactory()

    order_detail = repository.filter_by_id(order_detail_1.id)
    assert order_detail == order_detail_1

    order_detail = repository.filter_by_id(order_detail_2.id)
    assert order_detail == order_detail_2
