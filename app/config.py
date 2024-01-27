import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://postgres:password@postgres:5432/tails-coding-test-db",
    )
    POSTCODES_API_URL = os.getenv(
        "POSTCODES_API_URL", "https://api.postcodes.io/postcodes"
    )
    LOGGING_LEVEL = "INFO"
