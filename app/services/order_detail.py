from app.repositories.order_detail import OrderDetailRepository
from app.services.product import ProductService


class OrderDetailService:

    def __init__(
            self,
            order_detail_repository: OrderDetailRepository,
            product_service: ProductService,
    ):
        self._order_detail_repository = order_detail_repository
        self._product_service = product_service

    @classmethod
    def build(cls):
        return cls(
            order_detail_repository=OrderDetailRepository(),
            product_service=ProductService.build(),
        )

    def products_stock_restoring_process(self, order_detail_id: int):
        order_detail = self._order_detail_repository.filter_by_id(order_detail_id)

        self._product_service.add_stock(
            product_id=order_detail.product.id,
            quantity=order_detail.quantity
        )
