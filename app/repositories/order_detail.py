from app.models import OrderDetail


class OrderDetailRepository:

    def filter_by_id(self, order_detail_id: int) -> OrderDetail:
        return OrderDetail.objects.filter(id=order_detail_id).first()
