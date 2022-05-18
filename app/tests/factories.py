from datetime import datetime

import factory
import factory.fuzzy

from app.models import (
    Order,
    OrderDetail,
    Product,
)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("name")
    price = factory.fuzzy.FuzzyFloat(100, 1000)
    stock = factory.fuzzy.FuzzyInteger(1, 100)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    date_time = datetime.now()


class OrderDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderDetail

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 20)
    price = factory.fuzzy.FuzzyFloat(100, 1000)
