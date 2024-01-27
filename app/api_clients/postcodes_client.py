from dataclasses import dataclass
from typing import Any

import requests
from dataclasses_jsonschema import JsonSchemaMixin
from result import Err, Ok, Result

JsonDict = dict[str, Any]


@dataclass
class BaseType(JsonSchemaMixin):
    pass


@dataclass
class PostcodeData(BaseType):
    postcode: str
    eastings: int | None = None
    northings: int | None = None
    longitude: float | None = None
    latitude: float | None = None


@dataclass
class PostcodeResult(BaseType):
    query: str
    result: JsonDict | None = None


@dataclass
class APIResult(BaseType):
    status: int


@dataclass
class PostcodeLookupResult(APIResult):
    result: PostcodeData


@dataclass
class PostcodeBulkLookupResult(APIResult):
    result: list[PostcodeResult]


@dataclass
class APIError(APIResult):
    error: str


class PostcodesClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def postcode_lookup(
        self, postcode: str
    ) -> Result[PostcodeLookupResult, APIError]:
        url = f"{self.base_url}/{postcode}"
        result = requests.get(url)
        if result.status_code != 200:
            return Err(APIError.from_dict(result.json()))
        return Ok(PostcodeLookupResult.from_dict(result.json()))

    def bulk_postcode_lookup(
        self, postcodes: list[str]
    ) -> Result[PostcodeBulkLookupResult, APIError]:
        result = requests.post(self.base_url, json={"postcodes": postcodes})
        if result.status_code != 200:
            return Err(APIError.from_dict(result.json()))
        return Ok(PostcodeBulkLookupResult.from_dict(result.json()))
