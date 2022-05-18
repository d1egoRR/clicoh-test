import logging
from dataclasses import dataclass
from typing import Dict, Optional

import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework import status

from app.enumerations import USDType

logger = logging.getLogger(__name__)


@dataclass
class USDValueDTO:
    name: str
    value: float


class DolarSiGateway:
    _BASE_URL = 'https://www.dolarsi.com'

    def get_values(self) -> Optional[Dict]:
        url = f"{self._BASE_URL}/api/api.php?type=valoresprincipales"
        response = requests.get(url)

        if response.status_code != status.HTTP_200_OK:
            logger.exception(
                "Fail to get values for DolarSi",
                extra=dict(status_code=response.status_code)
            )
            return None

        return response.json()


class DolarSiParser:

    def parse_usd_value(
            self,
            usd_values: Dict,
            usd_type: USDType,
    ) -> Optional[USDValueDTO]:
        for value in usd_values:
            if value['casa']['nombre'] == usd_type.value:
                name = value['casa']['nombre']
                value = value['casa']['venta'].replace(',', '.')
                return USDValueDTO(
                    name=name, value=float(value),
                )

        return None


class DolarSiService:

    def __init__(
            self,
            gateway: DolarSiGateway,
            parser: DolarSiParser,
    ):
        self._gateway = gateway
        self._parser = parser

    @classmethod
    def build(cls):
        return cls(
            gateway=DolarSiGateway(),
            parser=DolarSiParser()
        )

    def calculate_total_usd(
            self,
            amount: float,
            usd_type: USDType,
    ) -> Optional[float]:
        usd_value = self.get_usd_value(usd_type)

        if usd_value is None:
            return None

        return round(amount / usd_value, 2)

    def get_usd_value(
            self,
            usd_type: USDType,
    ) -> Optional[float]:

        value = cache.get('usd_value')

        if value is not None:
            return value

        try:
            usd_values = self._gateway.get_values()

            if usd_values is not None:
                usd_value_dto = self._parser.parse_usd_value(
                    usd_values=usd_values,
                    usd_type=usd_type
                )

                cache.set(
                    'usd_value',
                    usd_value_dto.value,
                    settings.DOLAR_SI_CACHE_SECONDS
                )

                return usd_value_dto.value

        except Exception as e:
            logger.exception("Fail to get usd value for DolarSi")

        return None
