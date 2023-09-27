import json

import pytest
from sqlalchemy import text

from app import create_app
from app.data_types import StoreCollection
from app.models import Store
from app.models import db as _db


@pytest.fixture(scope="session")
def app():
    _app = create_app()
    _app.testing = True
    return _app


@pytest.fixture
def test_client(app, db):
    client = app.test_client()
    yield client


@pytest.fixture
def app_context(app):
    with app.app_context() as context:
        yield context


@pytest.fixture
def db(app_context):
    _db.session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
    _db.session.commit()
    _db.create_all()
    try:
        yield _db
    finally:
        _db.session.rollback()
        _db.drop_all()


def load_stores_json() -> StoreCollection:
    with open("tests/test_data/test_stores.json", "r") as f:
        data = json.load(f)
    return StoreCollection.from_dict(data)


@pytest.fixture
def populate_db(db):
    stores_data = load_stores_json()
    store_objects = [Store.from_dataclass(store) for store in stores_data]
    db.session.add_all(store_objects)
    db.session.commit()
