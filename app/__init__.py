from flask import Flask, redirect, request, url_for
from sqlalchemy import text

import app.views as views
from app.config import Config
from app.data_types import ViewType
from app.models import db
from app.utils import parse_view_type


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        db.create_all()

    app.add_url_rule("/<view_type>/", view_func=views.view_stores)
    app.add_url_rule("/<view_type>/filter/", view_func=views.filter_stores)

    @app.errorhandler(404)
    def redirect_not_found(e):
        return redirect(url_for("view_stores", view_type=ViewType.LIST.value))

    @app.before_request
    def pre_request_parse_view_type() -> None:
        if not request.view_args:
            return
        if view_type := request.view_args.get("view_type"):
            request.view_args["view_type"] = parse_view_type(view_type)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, use_reloader=True, port=8000)
