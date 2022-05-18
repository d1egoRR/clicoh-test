from rest_framework import serializers

from app.models import (
    Order,
    OrderDetail,
    Product,
)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'stock',
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'order',
            'product',
            'price',
            'quantity',
        )


class OrderSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(source="get_total", read_only=True)
    total_usd = serializers.FloatField(source="get_total_usd", read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'date_time',
            'total',
            'total_usd',
        )
