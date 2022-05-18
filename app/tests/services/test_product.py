import pytest

from app.services.product import ProductService
from app.tests.factories import ProductFactory


def test_build():
    ProductService.build()


@pytest.mark.django_db
def test_quantity_exists_in_stock():
    product_1 = ProductFactory(stock=20)
    product_2 = ProductFactory(stock=30)

    quantity = 25

    service = ProductService.build()
    quantity_exists_in_stock = service.quantity_exists_in_stock(
        product_id=product_1.id,
        quantity=quantity
    )

    assert not quantity_exists_in_stock

    quantity_exists_in_stock = service.quantity_exists_in_stock(
        product_id=product_2.id,
        quantity=quantity
    )

    assert quantity_exists_in_stock


@pytest.mark.django_db
def test_add_stock():
    product = ProductFactory(stock=20)

    quantity = 15

    service = ProductService.build()
    service.add_stock(product_id=product.id, quantity=quantity)

    product.refresh_from_db()
    assert product.stock == 35


@pytest.mark.django_db
def test_substract_stock():
    product = ProductFactory(stock=20)

    quantity = 5

    service = ProductService.build()
    service.substract_stock(product_id=product.id, quantity=quantity)

    product.refresh_from_db()
    assert product.stock == 15

    quantity = 30
    service.substract_stock(product_id=product.id, quantity=quantity)

    product.refresh_from_db()
    assert product.stock == 0
