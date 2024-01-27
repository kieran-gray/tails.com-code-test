from app import create_app
from app.models import db


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        tables = db.engine.table_names()
        assert "store" in tables