import pytest

from app.services.order_detail import OrderDetailService
from app.tests.factories import OrderDetailFactory, ProductFactory


def test_build():
    OrderDetailService.build()


@pytest.mark.django_db
def test_products_stock_restoring_process():
    product = ProductFactory(stock=10)
    order_detail = OrderDetailFactory(product=product, quantity=5)

    service = OrderDetailService.build()
    service.products_stock_restoring_process(
        order_detail_id=order_detail.id
    )

    product.refresh_from_db()
    assert product.stock == 15
