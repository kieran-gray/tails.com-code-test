from __future__ import annotations

from convertbng.util import convert_bng
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from shapely import Point
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import app.data_types as dt


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

GEOMETRY_SRID = 4326  # postcodes.io uses WGS84, EPSG 4326


class Store(Base):
    __tablename__ = "store"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    postcode: Mapped[str] = mapped_column(String, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    location: Mapped[str] = mapped_column(
        Geometry(geometry_type="POINT", srid=GEOMETRY_SRID, from_text="ST_GeomFromEWKT"), nullable=True
    )

    @classmethod
    def from_dataclass(cls, store: dt.Store) -> Store:
        return cls(
            name=store.name,
            postcode=store.postcode,
            longitude=store.longitude,
            latitude=store.latitude,
            location=Point(convert_bng(store.longitude, store.latitude)).wkt
            if store.longitude and store.latitude
            else None,
        )

    def to_dataclass(self) -> dt.Store:
        return dt.Store(
            name=self.name,
            postcode=self.postcode,
            longitude=self.longitude,
            latitude=self.latitude,
        )
