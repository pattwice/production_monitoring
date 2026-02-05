import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import AuthBase, ProdBase, get_auth_db, get_prod_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Pytest fixture to create a new database session for each test function.
    It creates all tables, yields a session, and then drops all tables.
    """
    AuthBase.metadata.create_all(bind=engine)
    ProdBase.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        AuthBase.metadata.drop_all(bind=engine)
        ProdBase.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    """
    Pytest fixture that provides a TestClient for making API requests.
    It overrides the database dependencies to use the in-memory test database.
    """

    def override_get_auth_db():
        try:
            yield db_session
        finally:
            db_session.close()

    def override_get_prod_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_auth_db] = override_get_auth_db
    app.dependency_overrides[get_prod_db] = override_get_prod_db

    yield TestClient(app)
    
    app.dependency_overrides = {}