from app.models import Order


class OrderRepository:

    def filter_by_id(self, order_id) -> Order:
        return Order.objects.filter(id=order_id).first()
