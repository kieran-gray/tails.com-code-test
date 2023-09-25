import json

from sqlalchemy import text
from sqlalchemy.orm import Session
from structlog import get_logger

import app.data_types as dt
from app import create_app
from app.api_clients.postcodes_client import PostcodeBulkLookupResult, PostcodesClient
from app.config import Config
from app.models import Store, db

logger = get_logger()

STORE_DATA_PATH = "data/stores.json"


def load_store_data_from_json(path: str) -> dt.StoreCollection:
    with open(path, "r") as f:
        json_data = json.load(f)
    return dt.StoreCollection([dt.Store.from_dict(store) for store in json_data])


def fetch_postcode_data(store_collection: dt.StoreCollection) -> None:
    client = PostcodesClient(Config.POSTCODES_API_URL)
    postcodes_result = client.bulk_postcode_lookup(store_collection.postcodes)
    if postcodes_result.is_err():
        logger.error(postcodes_result.unwrap_err().error)
        return
    postcodes_bulk_response: PostcodeBulkLookupResult = postcodes_result.unwrap()
    logger.info(f"Made bulk api postcodes API call with {len(store_collection.postcodes)} postcodes")
    for postcode_result in postcodes_bulk_response.result:
        if postcode_result.result:
            if store := store_collection.postcode_lookup(postcode_result.query):
                store.longitude = postcode_result.result.get("longitude")
                store.latitude = postcode_result.result.get("latitude")


def add_store_data_to_database(session: Session, store_collection: dt.StoreCollection) -> None:
    store_objects = [Store.from_dataclass(store) for store in store_collection]
    logger.info(f"Adding {len(store_objects)} to database")
    session.add_all(store_objects)
    session.commit()


def populate_store_data(session: Session, path: str = STORE_DATA_PATH) -> None:
    store_collection = load_store_data_from_json(path)
    fetch_postcode_data(store_collection)
    add_store_data_to_database(session, store_collection)


def wipe_store_table(session: Session) -> None:
    session.execute(text("TRUNCATE TABLE store"))
    session.commit()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        logger.info("Database populate script running")
        logger.info("Truncating store table")
        wipe_store_table(db.session)
        logger.info("Populating store table")
        populate_store_data(db.session)
        logger.info("Store table successfully populated")
