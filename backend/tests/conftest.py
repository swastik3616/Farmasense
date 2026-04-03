import pytest
import asyncio

from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app import create_app
from app.models.documents import (
    User, Admin, Farm, Advisory,
    AdvisoryReport, Alert, CommunityReport, DLQSms
)


# Create app fixture
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongodb://localhost:27017/test_farmsense",
        "RATELIMIT_ENABLED": False  # avoid 429 errors in tests
    })

    with app.app_context():
        yield app


# Initialize async DB (wrapped inside sync)
@pytest.fixture(autouse=True)
def mock_db(app):

    async def init_db():
        client = AsyncMongoMockClient()
        db = client.get_database("test_farmsense")

        # Patch for mongomock compatibility
        original = db.list_collection_names

        async def patched(*args, **kwargs):
            kwargs.pop("authorizedCollections", None)
            kwargs.pop("nameOnly", None)
            return await original(*args, **kwargs)

        db.list_collection_names = patched

        await init_beanie(
            database=db,
            document_models=[
                User, Admin, Farm, Advisory,
                AdvisoryReport, Alert, CommunityReport, DLQSms
            ]
        )

        app.db = db
        app.db_initialized = True

    # Run async DB setup
    asyncio.run(init_db())

    yield


# Use Flask test client (SYNC)
@pytest.fixture
def client(app):
    return app.test_client()


# CLI runner
@pytest.fixture
def runner(app):
    return app.test_cli_runner()