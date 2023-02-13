import logging
from datetime import datetime, timedelta

from sqlmodel import create_engine, Session, select

from app.core.settings import settings
from app.services import auth_service

from app.models.models import (
    AddressCreate,
    CustomerCreate,
    FitterCreate,
    FittingCreate,
    StoreCreate,
    Fitter,
    State,
    Role,
)
from app.db.repositories.address import AddressRepository
from app.db.repositories.customer import CustomerRepository
from app.db.repositories.fitter import FitterRepository
from app.db.repositories.fitting import FittingRepository
from app.db.repositories.store import StoreRepository

logger = logging.getLogger(__name__)


def init_data() -> None:
    engine = create_engine(settings.DB_URL)
    session = Session(engine)

    existing_lead_fitter = session.exec(
        select(Fitter).where(Fitter.role == Role.Lead)
    ).first()

    if not existing_lead_fitter:
        # Create addresses
        address_repo = AddressRepository(session=session)
        lead_fitter_1_address = AddressCreate(
            street="1 Lead Fitter Way",
            city="Store One",
            state=State.VA,
            zip_code=12345,
        )
        expert_fitter_1_address = AddressCreate(
            street="1 Expert Fitter Way",
            city="Store One",
            state=State.VA,
            zip_code=12345,
        )
        apprentice_fitter_1_address = AddressCreate(
            street="1 Apprentice Fitter Way",
            city="Store One",
            state=State.VA,
            zip_code=12345,
        )
        lead_fitter_2_address = AddressCreate(
            street="2 Lead Fitter Way",
            city="Store Two",
            state=State.MD,
            zip_code=67890,
        )
        expert_fitter_2_address = AddressCreate(
            street="2 Expert Fitter Way",
            city="Store Two",
            state=State.MD,
            zip_code=67890,
        )
        apprentice_fitter_2_address = AddressCreate(
            street="2 Apprentice Fitter Way",
            city="Store Two",
            state=State.MD,
            zip_code=67890,
        )
        store_1_address = AddressCreate(
            street="Store One Dr",
            city="Store One",
            state=State.VA,
            zip_code=12345,
        )
        store_2_address = AddressCreate(
            street="Store Two Dr",
            city="Store Two",
            state=State.MD,
            zip_code=67890,
        )
        customer_1_address = AddressCreate(
            street="1 Customer Way",
            city="Store One",
            state=State.VA,
            zip_code=12345,
        )
        customer_2_address = AddressCreate(
            street="2 Customer Way",
            city="Store One",
            state=State.VA,
            zip_code=12345,
        )
        customer_3_address = AddressCreate(
            street="3 Customer Way",
            city="Store One",
            state=State.VA,
            zip_code=12345,
        )
        customer_4_address = AddressCreate(
            street="4 Customer Way",
            city="Store Two",
            state=State.MD,
            zip_code=67890,
        )
        customer_5_address = AddressCreate(
            street="5 Customer Way",
            city="Store Two",
            state=State.MD,
            zip_code=67890,
        )
        customer_6_address = AddressCreate(
            street="6 Customer Way",
            city="Store Two",
            state=State.MD,
            zip_code=67890,
        )

        db_lead_fitter_1_address = address_repo.create_address(lead_fitter_1_address)
        db_expert_fitter_1_address = address_repo.create_address(
            expert_fitter_1_address
        )
        db_apprentice_fitter_1_address = address_repo.create_address(
            apprentice_fitter_1_address
        )
        db_lead_fitter_2_address = address_repo.create_address(lead_fitter_2_address)
        db_expert_fitter_2_address = address_repo.create_address(
            expert_fitter_2_address
        )
        db_apprentice_fitter_2_address = address_repo.create_address(
            apprentice_fitter_2_address
        )
        db_store_1_address = address_repo.create_address(store_1_address)
        db_store_2_address = address_repo.create_address(store_2_address)
        db_customer_1_address = address_repo.create_address(customer_1_address)
        db_customer_2_address = address_repo.create_address(customer_2_address)
        db_customer_3_address = address_repo.create_address(customer_3_address)
        db_customer_4_address = address_repo.create_address(customer_4_address)
        db_customer_5_address = address_repo.create_address(customer_5_address)
        db_customer_6_address = address_repo.create_address(customer_6_address)

        # Create stores
        store_repo = StoreRepository(session=session)

        store_1 = StoreCreate(
            name="Store One", phone="111-111-1111", address_id=db_store_1_address.id
        )
        store_2 = StoreCreate(
            name="Store Two", phone="222-222-2222", address_id=db_store_2_address.id
        )

        db_store_1 = store_repo.create_store(store_1)
        db_store_2 = store_repo.create_store(store_2)

        # Create customers
        customer_repo = CustomerRepository(session=session)

        customer_1 = CustomerCreate(
            first_name="Customer",
            last_name="One",
            email="customer.one@email.com",
            phone="111-111-1111",
            address_id=db_customer_1_address.id,
        )
        customer_2 = CustomerCreate(
            first_name="Customer",
            last_name="Two",
            email="customer.two@email.com",
            phone="222-222-2222",
            address_id=db_customer_2_address.id,
        )
        customer_3 = CustomerCreate(
            first_name="Customer",
            last_name="Three",
            email="customer.three@email.com",
            phone="333-333-3333",
            address_id=db_customer_3_address.id,
        )
        customer_4 = CustomerCreate(
            first_name="Customer",
            last_name="Four",
            email="customer.four@email.com",
            phone="444-444-4444",
            address_id=db_customer_4_address.id,
        )
        customer_5 = CustomerCreate(
            first_name="Customer",
            last_name="Five",
            email="customer.five@email.com",
            phone="555-555-5555",
            address_id=db_customer_5_address.id,
        )
        customer_6 = CustomerCreate(
            first_name="Customer",
            last_name="Six",
            email="customer.six@email.com",
            phone="666-666-6666",
            address_id=db_customer_6_address.id,
        )

        db_customer_1 = customer_repo.create_customer(customer_1)
        db_customer_2 = customer_repo.create_customer(customer_2)
        db_customer_3 = customer_repo.create_customer(customer_3)
        db_customer_4 = customer_repo.create_customer(customer_4)
        db_customer_5 = customer_repo.create_customer(customer_5)
        db_customer_6 = customer_repo.create_customer(customer_6)

        # Create fitters
        fitter_repo = FitterRepository(session=session)

        lead_fitter_1 = FitterCreate(
            username="lead1",
            password=auth_service.hash_password("password"),
            first_name="Lead",
            last_name="Fitter1",
            bio="This is Lead fitter one.",
            role=Role.Lead,
            store_id=db_store_1.id,
            address_id=db_lead_fitter_1_address.id,
        )
        expert_fitter_1 = FitterCreate(
            username="expert1",
            password=auth_service.hash_password("password"),
            first_name="Expert",
            last_name="Fitter1",
            bio="This is Expert fitter one.",
            role=Role.Expert,
            store_id=db_store_1.id,
            address_id=db_expert_fitter_1_address.id,
        )
        apprentice_fitter_1 = FitterCreate(
            username="apprentice1",
            password=auth_service.hash_password("password"),
            first_name="Apprentice",
            last_name="Fitter1",
            bio="This is Apprentice fitter one.",
            role=Role.Apprentice,
            store_id=db_store_1.id,
            address_id=db_apprentice_fitter_1_address.id,
        )
        lead_fitter_2 = FitterCreate(
            username="lead2",
            password=auth_service.hash_password("password"),
            first_name="Lead",
            last_name="Fitter2",
            bio="This is Lead fitter two.",
            role=Role.Lead,
            store_id=db_store_2.id,
            address_id=db_lead_fitter_2_address.id,
        )
        expert_fitter_2 = FitterCreate(
            username="expert2",
            password=auth_service.hash_password("password"),
            first_name="Expert",
            last_name="Fitter2",
            bio="This is Expert fitter two.",
            role=Role.Expert,
            store_id=db_store_2.id,
            address_id=db_expert_fitter_2_address.id,
        )
        apprentice_fitter_2 = FitterCreate(
            username="apprentice2",
            password=auth_service.hash_password("password"),
            first_name="Apprentice",
            last_name="Fitter2",
            bio="This is Apprentice fitter two.",
            role=Role.Apprentice,
            store_id=db_store_2.id,
            address_id=db_apprentice_fitter_2_address.id,
        )

        db_lead_fitter_1 = fitter_repo.create_fitter(lead_fitter_1)
        db_expert_fitter_1 = fitter_repo.create_fitter(expert_fitter_1)
        db_apprentice_fitter_1 = fitter_repo.create_fitter(apprentice_fitter_1)
        db_lead_fitter_2 = fitter_repo.create_fitter(lead_fitter_2)
        db_expert_fitter_2 = fitter_repo.create_fitter(expert_fitter_2)
        db_apprentice_fitter_2 = fitter_repo.create_fitter(apprentice_fitter_2)

        # Create fittings
        fitting_repo = FittingRepository(session=session)

        today = datetime.today()
        year, week_num, _ = today.isocalendar()
        monday = datetime.fromisocalendar(year, week_num, 1)
        monday_9am = monday + timedelta(hours=9)
        monday_10am = monday + timedelta(hours=10)
        monday_12pm = monday + timedelta(hours=12)
        monday_1pm = monday + timedelta(hours=13)
        tuesday = datetime.fromisocalendar(year, week_num, 2)
        tuesday_9am = tuesday + timedelta(hours=9)
        tuesday_10am = tuesday + timedelta(hours=10)
        tuesday_12pm = tuesday + timedelta(hours=12)
        tuesday_1pm = tuesday + timedelta(hours=13)
        wednesday = datetime.fromisocalendar(year, week_num, 3)
        wednesday_9am = wednesday + timedelta(hours=9)
        wednesday_10am = wednesday + timedelta(hours=10)
        wednesday_12pm = wednesday + timedelta(hours=12)
        wednesday_1pm = wednesday + timedelta(hours=13)

        fitting_1 = FittingCreate(
            start=monday_9am,
            end=monday_10am,
            text="Fitting One",
            barColor=db_lead_fitter_1.calendar_color,
            customer_id=db_customer_1.id,
            store_id=db_store_1.id,
            fitter_id=db_lead_fitter_1.id,
        )
        fitting_2 = FittingCreate(
            start=monday_12pm,
            end=monday_1pm,
            text="Fitting Two",
            barColor=db_expert_fitter_1.calendar_color,
            customer_id=db_customer_2.id,
            store_id=db_store_1.id,
            fitter_id=db_expert_fitter_1.id,
        )
        fitting_3 = FittingCreate(
            start=tuesday_9am,
            end=tuesday_10am,
            text="Fitting Three",
            barColor=db_apprentice_fitter_1.calendar_color,
            customer_id=db_customer_3.id,
            store_id=db_store_1.id,
            fitter_id=db_apprentice_fitter_1.id,
        )
        fitting_4 = FittingCreate(
            start=tuesday_12pm,
            end=tuesday_1pm,
            text="Fitting Four",
            barColor=db_lead_fitter_2.calendar_color,
            customer_id=db_customer_4.id,
            store_id=db_store_2.id,
            fitter_id=db_lead_fitter_2.id,
        )
        fitting_5 = FittingCreate(
            start=wednesday_9am,
            end=wednesday_10am,
            text="Fitting Five",
            barColor=db_expert_fitter_2.calendar_color,
            customer_id=db_customer_5.id,
            store_id=db_store_2.id,
            fitter_id=db_expert_fitter_2.id,
        )
        fitting_6 = FittingCreate(
            start=wednesday_12pm,
            end=wednesday_1pm,
            text="Fitting Six",
            barColor=db_apprentice_fitter_2.calendar_color,
            customer_id=db_customer_6.id,
            store_id=db_store_2.id,
            fitter_id=db_apprentice_fitter_2.id,
        )

        db_fitting_1 = fitting_repo.create_fitting(fitting_1)
        db_fitting_2 = fitting_repo.create_fitting(fitting_2)
        db_fitting_3 = fitting_repo.create_fitting(fitting_3)
        db_fitting_4 = fitting_repo.create_fitting(fitting_4)
        db_fitting_5 = fitting_repo.create_fitting(fitting_5)
        db_fitting_6 = fitting_repo.create_fitting(fitting_6)


def main():
    init_data()


if __name__ == "__main__":
    main()
