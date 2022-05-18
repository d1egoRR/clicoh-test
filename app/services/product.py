from app.models import Product
from app.repositories.product import ProductRepository


class ProductService:

    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository

    @classmethod
    def build(cls):
        return cls(
            product_repository=ProductRepository()
        )

    def quantity_exists_in_stock(
            self,
            product_id: int,
            quantity: int
    ) -> bool:
        product = self._product_repository.filter_by_id(product_id)
        return product.stock >= quantity

    def add_stock(self, product_id: int, quantity: int) -> Product:
        product = self._product_repository.filter_by_id(product_id)
        new_quantity = product.stock + quantity
        product = self._product_repository.update_stock(product_id, new_quantity)

        return product

    def substract_stock(self, product_id: int, quantity: int) -> Product:
        product = self._product_repository.filter_by_id(product_id)
        new_quantity = product.stock - quantity

        if new_quantity < 0:
            new_quantity = 0

        product = self._product_repository.update_stock(product_id, new_quantity)

        return product
