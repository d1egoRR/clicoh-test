import pytest
from django.urls import reverse
from rest_framework import status

from app.models import Product
from app.tests.factories import ProductFactory


def test_with_unlogged_client(unlogged_client):
    response = unlogged_client.get(reverse("products-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list(client_logged):
    response = client_logged.get(reverse("products-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['results'] == []

    ProductFactory(id=100, name='p1', price=11.5, stock=10)
    ProductFactory(id=200, name='p2', price=220.55, stock=30)

    response = client_logged.get(reverse("products-list"))

    expected_response = [
        dict(id=100, name='p1', price=11.5, stock=10),
        dict(id=200, name='p2', price=220.55, stock=30)
    ]
    response_results = response.json()['results']

    assert response.status_code == status.HTTP_200_OK
    assert response_results == expected_response


@pytest.mark.django_db
def test_detail(client_logged):
    ProductFactory(id=100, name='p1', price=11.5, stock=10)
    ProductFactory(id=200, name='p2', price=220.55, stock=30)

    response = client_logged.get(reverse("products-detail", args=(100,)))

    expected_response = dict(id=100, name='p1', price=11.5, stock=10)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_update(client_logged):
    ProductFactory(id=100, name='p1', price=11.5, stock=10)

    response = client_logged.put(
        reverse("products-detail", kwargs={'pk': 100}),
        data=dict(
            name='updated', price=20.55, stock=150
        )
    )

    expected_response = dict(id=100, name='updated', price=20.55, stock=150)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response


@pytest.mark.django_db
def test_delete(client_logged):
    ProductFactory(id=100, name='p1', price=11.5, stock=10)
    ProductFactory(id=200, name='p2', price=220.55, stock=30)

    response = client_logged.delete(reverse("products-detail", kwargs={'pk': 100}))

    assert Product.objects.count() == 1
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_update_stock(client_logged):
    ProductFactory(id=100, name='p1', price=11.5, stock=10)

    response = client_logged.post(
        reverse(
            "products-update-stock",
            kwargs={'pk': 100, 'quantity': 50}
        ),
    )

    expected_response = dict(id=100, name='p1', price=11.5, stock=50)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
