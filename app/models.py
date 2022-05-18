from datetime import datetime
from typing import Optional

from django.db import models
from django.db.models import F, Sum
from django.utils.translation import gettext as _

from app.enumerations import USDType
from app.services.dolar_si import DolarSiService


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField(blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(BaseModel):
    date_time = models.DateTimeField(default=datetime.now)

    @property
    def get_total(self) -> Optional[float]:
        details_with_subtotal = self.order_details.annotate(
            subtotal=F('price') * F('quantity')
        )
        result = details_with_subtotal.aggregate(total=Sum('subtotal'))
        return result['total']

    @property
    def get_total_usd(self) -> Optional[float]:
        service = DolarSiService.build()
        amount = self.get_total

        if amount is None:
            return None

        total_usd = service.calculate_total_usd(
            amount=amount,
            usd_type=USDType.BLUE
        )

        return total_usd

    def __str__(self):
        return str(self.date_time)


class OrderDetail(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_details'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_details'
    )
    price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return (
            f"{self.order} - {self.product} - ${self.price} ({self.quantity})"
        )

    class Meta:
        unique_together = ('order', 'product',)
