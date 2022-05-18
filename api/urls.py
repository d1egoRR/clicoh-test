from django.urls import include, path
from rest_framework import routers

from api import views


router = routers.SimpleRouter()
router.register(r'products', views.ProductModelViewSet, basename='products')
router.register(r'orders', views.OrderModelViewSet, basename='orders')
router.register(
    r'orderdetails',
    views.OrderDetailModelViewSet,
    basename='order_details'
)

urlpatterns = [
    path('', include(router.urls)),
]
