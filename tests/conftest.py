import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from database import get_session
from one_piece_api.app import app
from one_piece_api.models.user_model import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def test_user(session):
    test_user = User(
        username='teste_username field',
        email='teste_email.field@com.br',
        password='teste_password',
    )

    session.add(test_user)
    session.commit()
    session.refresh(test_user)

    return test_user
