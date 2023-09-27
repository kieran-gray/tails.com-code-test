import pytest

from app.data_types import (
    InvalidPostcodeError,
    InvalidRadiusError,
    MissingPostcodeError,
    MissingRadiusError,
    ViewType,
    validate_postcode,
    validate_radius,
)
from app.utils import parse_view_type


@pytest.mark.parametrize(
    "value,expected_result",
    [
        ("list", ViewType.LIST),
        ("LIST", ViewType.LIST),
        ("  MAP   ", ViewType.MAP),
        ("api", ViewType.API),
        ("test", ViewType.LIST),
        (1, ViewType.LIST),
        (None, ViewType.LIST),
    ],
)
def test_parse_view_type(value, expected_result):
    assert parse_view_type(value) is expected_result


@pytest.mark.parametrize(
    "value,raises_error",
    [
        ("HD7 5UZ", None),
        ("CH53QW", None),
        ("  SW1A 1AA   ", InvalidPostcodeError),
        ("je3 1ep", None),
        ("im94aj", None),
        ("test", InvalidPostcodeError),
        (1, InvalidPostcodeError),
        (None, MissingPostcodeError),
    ],
)
def test_validate_postcode(value, raises_error):
    if raises_error:
        with pytest.raises(raises_error):
            validate_postcode(value)
    else:
        validate_postcode(value)


@pytest.mark.parametrize(
    "value,raises_error",
    [
        (1.1, None),
        (-1231.12312, None),
        ("123f", InvalidRadiusError),
        (" ", InvalidRadiusError),
        (None, MissingRadiusError),
    ],
)
def test_validate_radius(value, raises_error):
    if raises_error:
        with pytest.raises(raises_error):
            validate_radius(value)
    else:
        validate_radius(value)
