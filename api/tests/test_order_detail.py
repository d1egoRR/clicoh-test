import pytest
from django.urls import reverse
from rest_framework import status

from app.models import OrderDetail
from app.tests.factories import (
    OrderFactory,
    OrderDetailFactory,
    ProductFactory,
)


def test_with_unlogged_client(unlogged_client):
    response = unlogged_client.get(reverse("order_details-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create(client_logged):
    order = OrderFactory()
    product_1 = ProductFactory(stock=20)

    assert OrderDetail.objects.count() == 0

    response = client_logged.post(
        reverse("order_details-list"),
        data=dict(
            order=order.id,
            product=product_1.id,
            price=20.55,
            quantity=10
        )
    )

    product_1.refresh_from_db()

    assert response.status_code == status.HTTP_201_CREATED
    assert OrderDetail.objects.count() == 1
    assert product_1.stock == 10

    order_detail = OrderDetail.objects.first()

    expected_response = dict(
        id=order_detail.id,
        order=order.id,
        product=product_1.id,
        price=20.55,
        quantity=10
    )

    assert response.json() == expected_response


@pytest.mark.django_db
def test_create_without_sock(client_logged):
    order = OrderFactory()
    product_1 = ProductFactory(stock=20)

    assert OrderDetail.objects.count() == 0

    response = client_logged.post(
        reverse("order_details-list"),
        data=dict(
            order=order.id,
            product=product_1.id,
            price=20.55,
            quantity=100
        )
    )

    product_1.refresh_from_db()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert OrderDetail.objects.count() == 0

    expected_response = dict(product='Insufficient stock')
    assert response.json() == expected_response


@pytest.mark.django_db
def test_delete(client_logged):
    product_1 = ProductFactory(stock=10)
    product_2 = ProductFactory(stock=30)

    order_detail_1 = OrderDetailFactory(id=1, product=product_1, quantity=5)
    order_detail_2 = OrderDetailFactory(id=2, product=product_2, quantity=10)

    response = client_logged.delete(
        reverse("order_details-detail", kwargs={'pk': order_detail_1.id})
    )

    product_1.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert OrderDetail.objects.count() == 1
    assert product_1.stock == 15

    response = client_logged.delete(
        reverse("order_details-detail", kwargs={'pk': order_detail_2.id})
    )

    product_2.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert OrderDetail.objects.count() == 0
    assert product_2.stock == 40
