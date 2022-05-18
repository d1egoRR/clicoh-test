import pytest

from app.services.order import OrderService
from app.tests.factories import (
    OrderFactory,
    OrderDetailFactory,
    ProductFactory,
)


def test_build():
    OrderService.build()


@pytest.mark.django_db
def test_products_stock_restoring_process():
    product_1 = ProductFactory(stock=10)
    product_2 = ProductFactory(stock=20)
    product_3 = ProductFactory(stock=30)

    order = OrderFactory()

    OrderDetailFactory(order=order, product=product_1, quantity=5)
    OrderDetailFactory(order=order, product=product_2, quantity=10)
    OrderDetailFactory(order=order, product=product_3, quantity=15)

    service = OrderService.build()
    service.products_stock_restoring_process(
        order_id=order.id
    )

    product_1.refresh_from_db()
    product_2.refresh_from_db()
    product_3.refresh_from_db()

    assert product_1.stock == 15
    assert product_2.stock == 30
    assert product_3.stock == 45
