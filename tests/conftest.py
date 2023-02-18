import os
import pytest
import alembic
from typing import Callable
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from alembic.config import Config

from app.models.models import *
from app.core.settings import settings
from app.services import auth_service
from app.server.dependencies.database import get_session
from app.server.dependencies.auth import active_fitter, lead_fitter
from app.db.repositories.address import AddressRepository
from app.db.repositories.store import StoreRepository
from app.db.repositories.fitter import FitterRepository


@pytest.fixture(scope="session")
def apply_migrations():
    os.environ["TESTING"] = "1"
    config = Config(file_="/fitter/app/alembic.ini")
    config.set_main_option("script_location", "/fitter/app/migrations")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture(scope="session")
def engine():
    _engine = create_engine(f"{settings.DB_URL}_test")
    yield _engine
    _engine.dispose()
    _engine = None


@pytest.fixture
def session(engine) -> Session:
    _session = Session(engine)
    yield _session
    _session.close()


@pytest.fixture
def get_session_dep(session: Session) -> Callable:
    def get_session():
        return session

    return get_session


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.server.server import get_application

    _app = get_application()
    yield _app
    _app.dependency_overrides = []


@pytest.fixture
def store_address(session: Session) -> AddressRead:
    address_repo = AddressRepository(session=session)
    address_create = AddressCreate(
        street="Store One Way", city="Store One", state=State.AK, zip_code=12345
    )
    return address_repo.create_address(address_create=address_create)


@pytest.fixture
def lead_fitter_address(session: Session) -> AddressRead:
    address_repo = AddressRepository(session=session)
    address_create = AddressCreate(
        street="Lead Fitter Way", city="Lead Fitter", state=State.AK, zip_code=12345
    )
    return address_repo.create_address(address_create=address_create)


@pytest.fixture
def expert_fitter_address(session: Session) -> AddressRead:
    address_repo = AddressRepository(session=session)
    address_create = AddressCreate(
        street="Expert Fitter Way", city="Expert Fitter", state=State.AK, zip_code=12345
    )
    return address_repo.create_address(address_create=address_create)


@pytest.fixture
def test_store(session: Session, store_address: AddressRead) -> StoreRead:
    store_repo = StoreRepository(session=session)
    store_create = StoreCreate(
        name="Store One", phone="111-111-1111", address_id=store_address.id
    )
    return store_repo.create_store(store_create=store_create)


@pytest.fixture
def test_lead_fitter(
    session: Session, lead_fitter_address: AddressRead, test_store: StoreRead
) -> FitterRead:
    fitter_repo = FitterRepository(session=session)
    fitter_create = FitterCreate(
        username="lead1",
        password=auth_service.hash_password("password"),
        first_name="Lead",
        last_name="Fitter",
        bio="This is a Lead fitter.",
        role=Role.Lead,
        store_id=test_store.id,
        address_id=lead_fitter_address.id,
    )
    db_fitter = fitter_repo.create_fitter(fitter_create=fitter_create)
    yield db_fitter
    fitter_repo.delete_fitter(fitter_id=db_fitter.id)


@pytest.fixture
def test_expert_fitter(
    session: Session, expert_fitter_address: AddressRead, test_store: StoreRead
) -> FitterRead:
    fitter_repo = FitterRepository(session=session)
    fitter_create = FitterCreate(
        username="expert1",
        password=auth_service.hash_password("password"),
        first_name="Expert",
        last_name="Fitter",
        bio="This is an Expert fitter.",
        role=Role.Expert,
        store_id=test_store.id,
        address_id=expert_fitter_address.id,
    )
    db_fitter = fitter_repo.create_fitter(fitter_create=fitter_create)
    yield db_fitter
    fitter_repo.delete_fitter(fitter_id=db_fitter.id)


@pytest.fixture
def expert_fitter_dep(test_expert_fitter: FitterRead) -> Callable:
    def expert_fitter():
        return test_expert_fitter

    return expert_fitter


@pytest.fixture
def expert_client(app: FastAPI, expert_fitter_dep, get_session_dep) -> TestClient:
    app.dependency_overrides[get_session] = get_session_dep
    app.dependency_overrides[active_fitter] = expert_fitter_dep
    client = TestClient(app)
    return client


@pytest.fixture
def lead_fitter_dep(test_lead_fitter: FitterRead) -> Callable:
    def lead_fitter():
        return test_lead_fitter

    return lead_fitter


@pytest.fixture
def lead_client(app: FastAPI, lead_fitter_dep, get_session_dep) -> TestClient:
    app.dependency_overrides[get_session] = get_session_dep
    app.dependency_overrides[active_fitter] = lead_fitter_dep
    client = TestClient(app)
    return client
