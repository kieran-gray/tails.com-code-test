from json import dumps

from flask import Response, render_template, request

from app.data_queries import (
    fetch_postcode_data,
    get_bbox,
    get_stores,
    get_stores_in_radius,
)
from app.data_types import FilterViewContext, ViewContext, ViewType
from app.utils import (
    get_lat_lng_from_postcode_data,
    get_point_from_postcode_data,
)


def view_stores(view_type: ViewType):
    bbox = get_bbox() if view_type is ViewType.MAP else None
    view_context = ViewContext(
        view_type=view_type.value, stores=get_stores(), bbox=bbox
    )

    if view_type is ViewType.API:
        return view_context.stores.to_dict()
    return render_template(f"{view_type.value}.html", **view_context.__dict__)


def filter_stores(view_type: ViewType):
    view_context = FilterViewContext(
        view_type.value,
        postcode=request.args.get("postcode", ""),
        radius_str=request.args.get("radius", ""),
        bbox=get_bbox() if view_type is ViewType.MAP else None,
    )

    if view_context.errors:
        if view_type is ViewType.API:
            return Response(
                dumps(str(view_context.errors)),
                status=400,
                mimetype="application/json",
            )
        view_context.stores = get_stores()
        return render_template(
            f"{view_type.value}.html", **view_context.__dict__
        )

    postcode_data = fetch_postcode_data(view_context.postcode)
    if not postcode_data:
        view_context.errors["postcode"] = "Postcode not found"
        if view_type is ViewType.API:
            return Response(
                dumps(str(view_context.errors)),
                status=404,
                mimetype="application/json",
            )
        view_context.stores = get_stores()
        return render_template(
            f"{view_type.value}.html", **view_context.__dict__
        )

    assert view_context.radius
    point = get_point_from_postcode_data(postcode_data)
    view_context.search_location = get_lat_lng_from_postcode_data(
        postcode_data
    )
    view_context.stores = get_stores_in_radius(point, view_context.radius)

    if view_type is ViewType.API:
        return Response(
            view_context.stores.to_json(),
            status=200,
            mimetype="application/json",
        )
    return render_template(f"{view_type.value}.html", **view_context.__dict__)
