import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from database import get_session
from one_piece_api.app import app
from one_piece_api.models.user_model import User, table_registry
from security import get_password_hash


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
def generate_test_token(client, test_user):
    response = client.post(
        '/auth/token',
        data={'username': test_user.username, 'password': test_user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def test_user(session):
    pwd = 'teste_password.12345'

    test_user = UserFactory(
        password=get_password_hash(pwd),
    )

    session.add(test_user)
    session.commit()
    session.refresh(test_user)

    test_user.clean_password = pwd
    return test_user


@pytest.fixture
def test_other_user(session):
    test_other_user = UserFactory()

    session.add(test_other_user)
    session.commit()
    session.refresh(test_other_user)
    return test_other_user


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@emailtest.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.email}_123pwd')
