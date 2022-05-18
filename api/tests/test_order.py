from datetime import datetime
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from app.models import Order, OrderDetail
from app.tests.factories import (
    OrderFactory,
    OrderDetailFactory,
    ProductFactory,
)


def test_with_unlogged_client(unlogged_client):
    response = unlogged_client.get(reverse("orders-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@patch("app.models.DolarSiService.get_usd_value")
def test_list(patched_dolar_si_service_get_usd_value, client_logged):
    usd_blue_value = 207.0
    patched_dolar_si_service_get_usd_value.return_value = usd_blue_value

    response = client_logged.get(reverse("orders-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'] == []

    product_1 = ProductFactory()
    product_2 = ProductFactory()
    product_3 = ProductFactory()

    order_1 = OrderFactory(id=1, date_time=datetime.now())
    order_2 = OrderFactory(id=2, date_time=datetime.now())

    OrderDetailFactory(order=order_1, product=product_1, price=150, quantity=2)
    OrderDetailFactory(order=order_1, product=product_2, price=160, quantity=3)
    OrderDetailFactory(order=order_2, product=product_1, price=150, quantity=1)
    OrderDetailFactory(order=order_2, product=product_3, price=120, quantity=2)

    response = client_logged.get(reverse("orders-list"))

    expected_total_1 = 780.0
    expected_total_usd_1 = round(expected_total_1 / usd_blue_value, 2)

    expected_total_2 = 390.0
    expected_total_usd_2 = round(expected_total_2 / usd_blue_value, 2)

    expected_response = [
        dict(
            id=order_1.id,
            date_time=order_1.date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            total=expected_total_1,
            total_usd=expected_total_usd_1
        ),
        dict(
            id=order_2.id,
            date_time=order_2.date_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            total=expected_total_2,
            total_usd=expected_total_usd_2
        ),
    ]

    response_results = response.json()['results']

    assert response.status_code == status.HTTP_200_OK
    assert len(response_results) == 2
    assert response_results == expected_response


@pytest.mark.django_db
def test_delete(client_logged):
    product_1 = ProductFactory(stock=10)
    product_2 = ProductFactory(stock=30)

    order = OrderFactory(id=1)

    OrderDetailFactory(order=order, product=product_1, quantity=5)
    OrderDetailFactory(order=order, product=product_2, quantity=10)

    response = client_logged.delete(
        reverse("orders-detail", kwargs={'pk': order.id})
    )

    product_1.refresh_from_db()
    product_2.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Order.objects.count() == 0
    assert OrderDetail.objects.count() == 0
    assert product_1.stock == 15
    assert product_2.stock == 40
