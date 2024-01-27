from re import compile
from typing import Sequence

from convertbng.util import convert_lonlat
from shapely import Point
from sqlalchemy import select, text
from structlog import get_logger

import app.data_types as dt
from app.api_clients.postcodes_client import PostcodeData, PostcodesClient
from app.config import Config
from app.models import Store, db

logger = get_logger()

WKT_REGEX = compile(r"-?(?:\.\d+|\d+(?:\.\d*)?)")


def get_stores() -> dt.StoreCollection:
    stores: Sequence[Store] = db.session.execute(
        db.select(Store).order_by(Store.name.asc())
    ).scalars()
    return dt.StoreCollection([store.to_dataclass() for store in stores])


def fetch_postcode_data(postcode: str) -> PostcodeData | None:
    client = PostcodesClient(Config.POSTCODES_API_URL)
    result = client.postcode_lookup(postcode)
    if result.is_err():
        logger.error(result.unwrap_err().error)
        return None
    return result.unwrap().result


def get_stores_in_radius(point: Point, radius: float) -> dt.StoreCollection:
    radius_m = radius * 1000
    query = text(
        """
        SELECT * FROM store WHERE
        ST_DWithin(
            ST_GeomFromEWKB(location),
            ST_SetSRID(ST_GeomFromText(:point_wkt), 4326),
            :radius
        )
        ORDER BY latitude DESC
        """
    )
    stmt = select(Store).from_statement(query)
    stores = db.session.execute(
        stmt, {"point_wkt": point.wkt, "radius": radius_m}
    ).scalars()
    return dt.StoreCollection([store.to_dataclass() for store in stores])


def get_bbox() -> dt.BBox | None:
    bbox = db.session.execute(
        text("SELECT ST_Extent(location) as bbox FROM store")
    ).fetchall()[0][0]
    if not bbox:
        logger.error("No BBox found. Is database empty?")
        return None
    coords = WKT_REGEX.findall(bbox)
    return (
        convert_lonlat(float(coords[0]), float(coords[1])),
        convert_lonlat(float(coords[2]), float(coords[3])),
    )
