from dataclasses import dataclass, field
from enum import Enum
from re import compile
from typing import Any, Iterator

from dataclasses_jsonschema import JsonSchemaMixin

JsonDict = dict[str, Any]
LatLng = tuple[float, float]
BBox = tuple[LatLng, LatLng]

POSTCODE_REGEX = compile(r"^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] 0[Aa]{2})$")


class BaseType(JsonSchemaMixin):
    pass


class InvalidPostcodeError(ValueError):
    pass


class InvalidRadiusError(ValueError):
    pass


class MissingPostcodeError(ValueError):
    pass


class MissingRadiusError(ValueError):
    pass


class ViewType(Enum):
    LIST = "list"
    MAP = "map"
    API = "api"


@dataclass(slots=True)
class Store(BaseType):
    name: str
    postcode: str
    longitude: float | None = None
    latitude: float | None = None

    def __post_init__(self):
        self.postcode = self.format_postcode()

    def format_postcode(self) -> str:
        postcode = self.postcode.upper().strip()
        cull_point = len(postcode) - 3
        if " " not in postcode:
            postcode = postcode.replace(postcode[cull_point:], " " + postcode[cull_point:])
        return postcode


@dataclass(slots=True)
class StoreCollection(BaseType):
    stores: list[Store] = field(default_factory=list)
    store_dict: dict[str, Store] | None = None

    def __len__(self) -> int:
        return len(self.stores)

    def __iter__(self) -> Iterator[Store]:
        for store in self.stores:
            yield store

    @property
    def postcodes(self) -> list[str]:
        return [store.postcode for store in self.stores]

    def postcode_lookup(self, postcode: str) -> Store | None:
        if not self.store_dict:
            self.store_dict = {store.postcode: store for store in self.stores}
        return self.store_dict.get(postcode)


@dataclass(slots=True, frozen=True)
class GetStoresResponse(BaseType):
    stores: list[Store] = field(default_factory=list)


@dataclass
class ViewContext:
    view_type: str
    stores: StoreCollection = field(default_factory=StoreCollection)
    bbox: BBox | None = None


@dataclass
class FilterViewContext(ViewContext):
    postcode: str = ""
    radius_str: str = ""
    radius: float | None = None
    errors: JsonDict = field(default_factory=dict)
    search_location: LatLng | None = None

    def __post_init__(self):
        try:
            validate_postcode(self.postcode)
        except (MissingPostcodeError, InvalidPostcodeError) as err:
            self.errors["postcode"] = str(err)
        try:
            validate_radius(self.radius_str)
            self.radius = float(self.radius_str)
        except (MissingRadiusError, InvalidRadiusError) as err:
            self.errors["radius"] = str(err)


def validate_postcode(postcode: str) -> None:
    if not postcode:
        raise MissingPostcodeError("Postcode is a required field")
    if not isinstance(postcode, str) or POSTCODE_REGEX.match(postcode) is None:
        raise InvalidPostcodeError(f"`{postcode}` is not a valid postcode")


def validate_radius(radius: str) -> None:
    if not radius:
        raise MissingRadiusError("Radius is a required field")
    try:
        float(radius)
    except ValueError:
        raise InvalidRadiusError(f"{radius} is not a valid radius. Must be type Float")
