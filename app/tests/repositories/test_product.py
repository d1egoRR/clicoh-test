import pytest

from app.repositories.product import ProductRepository
from app.tests.factories import ProductFactory


@pytest.mark.django_db
def test_filter_by_id():
    product_id_not_existing = 1

    repository = ProductRepository()
    product = repository.filter_by_id(product_id_not_existing)

    assert product is None

    product_1 = ProductFactory()
    product_2 = ProductFactory()

    product = repository.filter_by_id(product_1.id)
    assert product == product_1

    product = repository.filter_by_id(product_2.id)
    assert product == product_2


@pytest.mark.django_db
def test_update_stock():
    product = ProductFactory(stock=15)
    new_quantity = 20

    repository = ProductRepository()
    repository.update_stock(
        product_id=product.id,
        quantity=new_quantity
    )

    product.refresh_from_db()

    assert product.stock == new_quantity
