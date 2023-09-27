from convertbng.util import convert_bng, convert_lonlat
from shapely import Point

from app.api_clients.postcodes_client import PostcodeData
from app.data_types import LatLng, ViewType


def get_point_from_postcode_data(postcode_data: PostcodeData) -> Point | None:
    if postcode_data.eastings and postcode_data.northings:
        return Point(postcode_data.eastings, postcode_data.northings)
    elif postcode_data.longitude and postcode_data.latitude:
        return Point(convert_bng(postcode_data.longitude, postcode_data.latitude))
    return None


def get_lat_lng_from_postcode_data(postcode_data: PostcodeData) -> LatLng | None:
    if postcode_data.eastings and postcode_data.northings:
        return convert_lonlat(float(postcode_data.eastings), float(postcode_data.northings))
    elif postcode_data.longitude and postcode_data.latitude:
        return convert_bng(postcode_data.longitude, postcode_data.latitude)
    return None


def parse_view_type(view_type: str) -> ViewType:
    try:
        return ViewType(view_type.strip().lower())
    except (ValueError, AttributeError):
        return ViewType.LIST
