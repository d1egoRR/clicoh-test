from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    OrderSerializer,
    OrderDetailSerializer,
    ProductSerializer,
)
from app.models import (
    Order,
    OrderDetail,
    Product,
)
from app.repositories.product import ProductRepository
from app.services.order import OrderService
from app.services.order_detail import OrderDetailService
from app.services.product import ProductService


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(
        detail=True,
        methods=("POST",),
        url_path="update-stock/(?P<quantity>[^/.]+)",
        name="Update stock to product"
    )
    def update_stock(self, request, quantity, *args, **kwargs):
        instance = self.get_object()
        product_repository = ProductRepository()

        product = product_repository.update_stock(
            product_id=instance.id,
            quantity=quantity
        )

        serializer = ProductSerializer(product)
        return Response(serializer.data)


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        order_service = OrderService.build()

        order_service.products_stock_restoring_process(
            order_id=instance.id
        )

        return super().destroy(request, *args, **kwargs)


class OrderDetailModelViewSet(ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = OrderDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer['product'].value
        quantity = serializer['quantity'].value

        product_service = ProductService.build()

        if not product_service.quantity_exists_in_stock(product_id, quantity):
            return Response(
                dict(product="Insufficient stock"),
                status=status.HTTP_400_BAD_REQUEST
            )

        product_service.substract_stock(
            product_id=product_id,
            quantity=quantity
        )

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        order_detail_service = OrderDetailService.build()

        order_detail_service.products_stock_restoring_process(
            order_detail_id=instance.id
        )

        return super().destroy(request, *args, **kwargs)
