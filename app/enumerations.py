from enum import unique, Enum


@unique
class USDType(Enum):
    BLUE = "Dolar Blue"
    OFFICIAL = "Dolar Oficial"
    SOY = "Dolar Soja"
