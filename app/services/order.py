from app.repositories.order import OrderRepository
from app.services.order_detail import OrderDetailService


class OrderService:

    def __init__(
            self,
            order_detail_service: OrderDetailService,
            order_repository: OrderRepository,
    ):
        self._order_detail_service = order_detail_service
        self._order_repository = order_repository

    @classmethod
    def build(cls):
        return cls(
            order_detail_service=OrderDetailService.build(),
            order_repository=OrderRepository(),
        )

    def products_stock_restoring_process(self, order_id: int):
        order = self._order_repository.filter_by_id(order_id)
        order_details = order.order_details.all()

        for detail in order_details.iterator():
            self._order_detail_service.products_stock_restoring_process(
                order_detail_id=detail.id
            )
