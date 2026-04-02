import pytest
import asyncio
from httpx import AsyncClient
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from mongomock_motor import AsyncMongoMockClient

from app import create_app
from app.models.documents import User, Admin, Farm, Advisory, AdvisoryReport, Alert, CommunityReport, DLQSms

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def app():
    """Create and configure a new app instance for each test suite."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongodb://localhost:27017/test_farmsense",
    })
    
    # Push app context so that current_app and other extensions work in tests
    with app.app_context():
        yield app

@pytest.fixture(autouse=True)
async def mock_db(app):
    """
    Initialize a mocked MongoDB client and configure Beanie for all tests.
    Drops all data after each test to ensure isolation.
    """
    client = AsyncMongoMockClient()
    db = client.get_database("test_farmsense")
    
    # Patch list_collection_names to handle mongomock/beanie incompatibility
    # beanie (1.21.0+) uses authorizedCollections=True and nameOnly which mongomock doesn't support
    original_list_collection_names = db.list_collection_names
    async def patched_list_collection_names(*args, **kwargs):
        kwargs.pop("authorizedCollections", None)
        kwargs.pop("nameOnly", None)
        return await original_list_collection_names(*args, **kwargs)
    db.list_collection_names = patched_list_collection_names

    await init_beanie(database=db, document_models=[
        User, Admin, Farm, Advisory, AdvisoryReport, Alert, CommunityReport, DLQSms
    ])
    
    app.db = db
    app.db_initialized = True
    
    yield
    
    # Teardown
    await db.client.drop_database("test_farmsense")

@pytest.fixture
def client(app):
    """A synchronous test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's script commands."""
    return app.test_cli_runner()
