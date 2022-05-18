from unittest.mock import patch

import pytest

from app.tests.factories import (
    OrderFactory,
    OrderDetailFactory,
    ProductFactory,
)


@pytest.mark.django_db
def test_get_total():
    order = OrderFactory()

    assert order.get_total is None

    product_1 = ProductFactory()
    product_2 = ProductFactory()
    product_3 = ProductFactory()

    OrderDetailFactory(
        order=order, product=product_1, price=250, quantity=1
    )
    OrderDetailFactory(
        order=order, product=product_2, price=420, quantity=2
    )
    OrderDetailFactory(
        order=order, product=product_3, price=340, quantity=1
    )

    expected_total = 1430
    assert order.get_total == expected_total


@pytest.mark.django_db
@patch("app.models.DolarSiService.get_usd_value")
def test_get_total_usd(patched_dolar_si_service_get_usd_value):
    usd_blue_value = 207.0
    patched_dolar_si_service_get_usd_value.return_value = usd_blue_value

    order = OrderFactory()

    assert order.get_total_usd is None

    product_1 = ProductFactory()
    product_2 = ProductFactory()
    product_3 = ProductFactory()

    OrderDetailFactory(
        order=order, product=product_1, price=250, quantity=1
    )
    OrderDetailFactory(
        order=order, product=product_2, price=420, quantity=2
    )
    OrderDetailFactory(
        order=order, product=product_3, price=340, quantity=1
    )

    expected_total_usd = round(1430 / usd_blue_value, 2)
    assert order.get_total_usd == expected_total_usd
