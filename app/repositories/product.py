from typing import Optional

from app.models import Product


class ProductRepository:

    def filter_by_id(self, product_id: int) -> Optional[Product]:
        return Product.objects.filter(id=product_id).first()

    def update_stock(self, product_id: int, quantity: int) -> Product:
        product = self.filter_by_id(product_id)
        product.stock = quantity
        product.save()

        return product
