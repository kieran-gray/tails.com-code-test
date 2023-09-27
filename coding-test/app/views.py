from json import dumps

from flask import Response, render_template, request

from app.data_queries import (
    fetch_postcode_data,
    get_bbox,
    get_stores,
    get_stores_in_radius,
)
from app.data_types import FilterViewContext, ViewType
from app.utils import (
    get_lat_lng_from_postcode_data,
    get_point_from_postcode_data,
    parse_view_type,
)


def view_stores(view_type: str):
    view_type_enum = parse_view_type(view_type)
    stores = get_stores()

    if view_type_enum is ViewType.API:
        return stores.to_dict()

    return render_template(
        "map.html" if view_type_enum is ViewType.MAP else "index.html",
        view_type=view_type_enum.value,
        stores=stores,
        bbox=get_bbox() if view_type_enum is ViewType.MAP else None,
    )


def filter_stores(view_type: str):
    view_type_enum = parse_view_type(view_type)
    template = "map.html" if view_type_enum is ViewType.MAP else "index.html"
    view_context = FilterViewContext(
        view_type_enum.value,
        postcode=request.args.get("postcode", ""),
        radius_str=request.args.get("radius", ""),
        bbox=get_bbox() if view_type_enum is ViewType.MAP else None,
    )

    if view_context.errors:
        if view_type_enum is ViewType.API:
            return Response(dumps(str(view_context.errors)), status=400, mimetype="application/json")
        view_context.stores = get_stores()
        return render_template(template, **view_context.to_dict())

    postcode_data = fetch_postcode_data(view_context.postcode)
    if not postcode_data:
        # Postcode not found
        view_context.errors = {"postcode": "Postcode not found"}
        if view_type_enum is ViewType.API:
            return Response(dumps(str(view_context.errors)), status=404, mimetype="application/json")
        view_context.stores = get_stores()
        return render_template(template, **view_context.to_dict())

    point = get_point_from_postcode_data(postcode_data)
    view_context.search_location = get_lat_lng_from_postcode_data(postcode_data)
    assert view_context.radius
    view_context.stores = get_stores_in_radius(point, view_context.radius)

    if view_type_enum is ViewType.API:
        return Response(view_context.stores.to_json(), status=200, mimetype="application/json")
    return render_template(template, **view_context.to_dict())
