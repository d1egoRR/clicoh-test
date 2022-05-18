import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from rest_framework import status

from app.enumerations import USDType
from app.services.dolar_si import (
    DolarSiGateway,
    DolarSiParser,
    DolarSiService,
)


def test_build_service():
    DolarSiService.build()


@patch('requests.get')
def test_gateway_get_values(patched_requests_get):
    response = Mock(status_code=status.HTTP_200_OK)
    patched_requests_get.return_value = response

    gateway = DolarSiGateway()
    gateway.get_values()

    patched_requests_get.assert_called_once_with(
        'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
    )


@patch('requests.get')
def test_gateway_get_values_exception(patched_requests_get):
    response = Mock(status_code=status.HTTP_400_BAD_REQUEST)
    patched_requests_get.return_value = response

    gateway = DolarSiGateway()
    values_json = gateway.get_values()

    assert values_json is None


def test_parser_parse_usd_value():
    fixture_dir = Path(__file__).parent.joinpath("fixtures").as_posix()
    fixture_file = f"{fixture_dir}/dolar_si_values.json"

    with open(fixture_file, "r") as content:
        usd_values = json.loads(content.read())

    parser = DolarSiParser()
    usd_value_dto = parser.parse_usd_value(
        usd_values=usd_values,
        usd_type=USDType.BLUE
    )

    assert usd_value_dto.name == 'Dolar Blue'
    assert usd_value_dto.value == 207.0


def test_parser_parse_usd_value_without_dolar_blue():
    fixture_dir = Path(__file__).parent.joinpath("fixtures").as_posix()
    fixture_file = f"{fixture_dir}/dolar_si_values_without_dolar_blue.json"

    with open(fixture_file, "r") as content:
        usd_values = json.loads(content.read())

    parser = DolarSiParser()
    usd_value_dto = parser.parse_usd_value(
        usd_values=usd_values,
        usd_type=USDType.BLUE
    )

    assert usd_value_dto is None


def test_service_get_usd_value():
    fixture_dir = Path(__file__).parent.joinpath("fixtures").as_posix()
    fixture_file = f"{fixture_dir}/dolar_si_values.json"

    with open(fixture_file, "r") as content:
        usd_values = json.loads(content.read())

    mocked_gateway = Mock(spec_set=DolarSiGateway)
    mocked_gateway.get_values.return_value = usd_values

    service = DolarSiService(
        gateway=mocked_gateway,
        parser=DolarSiParser()
    )

    value = service.get_usd_value(usd_type=USDType.BLUE)

    assert value == 207.0

    value = service.get_usd_value(usd_type=USDType.OFFICIAL)

    assert value == 123.27


def test_service_get_usd_value_without_dolar_blue():
    fixture_dir = Path(__file__).parent.joinpath("fixtures").as_posix()
    fixture_file = f"{fixture_dir}/dolar_si_values_without_dolar_blue.json"

    with open(fixture_file, "r") as content:
        usd_values = json.loads(content.read())

    mocked_gateway = Mock(spec_set=DolarSiGateway)
    mocked_gateway.get_values.return_value = usd_values

    service = DolarSiService(
        gateway=mocked_gateway,
        parser=DolarSiParser()
    )

    value = service.get_usd_value(usd_type=USDType.BLUE)

    assert value is None


def test_service_calculate_total_usd():
    fixture_dir = Path(__file__).parent.joinpath("fixtures").as_posix()
    fixture_file = f"{fixture_dir}/dolar_si_values.json"

    with open(fixture_file, "r") as content:
        usd_values = json.loads(content.read())

    mocked_gateway = Mock(spec_set=DolarSiGateway)
    mocked_gateway.get_values.return_value = usd_values

    service = DolarSiService(
        gateway=mocked_gateway,
        parser=DolarSiParser()
    )

    total_usd = service.calculate_total_usd(
        amount=2500, usd_type=USDType.BLUE
    )

    expected_total_usd = round(2500 / 207.0, 2)

    assert total_usd == expected_total_usd


def test_service_calculate_total_usd_without_dolar_blue():
    fixture_dir = Path(__file__).parent.joinpath("fixtures").as_posix()
    fixture_file = f"{fixture_dir}/dolar_si_values_without_dolar_blue.json"

    with open(fixture_file, "r") as content:
        usd_values = json.loads(content.read())

    mocked_gateway = Mock(spec_set=DolarSiGateway)
    mocked_gateway.get_values.return_value = usd_values

    service = DolarSiService(
        gateway=mocked_gateway,
        parser=DolarSiParser()
    )

    total_usd = service.calculate_total_usd(
        amount=2500, usd_type=USDType.BLUE
    )

    assert total_usd is None
