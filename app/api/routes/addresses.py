from typing import List
from fastapi import Depends, APIRouter

from app.api.dependencies.database import get_repository
from app.models.address import AddressCreate, AddressRead, AddressUpdate
from app.db.repositories.address import AddressRepository


addresses_router = APIRouter(prefix="/addresses", tags=["addresses"])


@addresses_router.get(
    "",
    response_model=List[AddressRead],
    name="addresses:get-addresses",
)
async def get_addresses(
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
) -> List[AddressRead]:
    return address_repo.get_all_addresses()


@addresses_router.post(
    "",
    response_model=AddressRead,
    name="addresses:create-address",
)
async def create_address(
    *,
    address_create: AddressCreate,
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
) -> AddressRead:
    return address_repo.create_address(address_create=address_create)


@addresses_router.get(
    "/{address_id}",
    response_model=AddressRead,
    name="addresses:get-address",
)
async def get_address(
    *,
    address_id: int,
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
) -> AddressRead:
    return address_repo.get_address_by_id(address_id=address_id)


@addresses_router.put(
    "/{address_id}",
    response_model=AddressRead,
    name="addresses:update-address",
)
async def update_address(
    *,
    address_id: int,
    address_update: AddressUpdate,
    address_repo: AddressRepository = Depends(get_repository(AddressRepository)),
) -> AddressRead:
    return address_repo.update_address(
        address_update=address_update, address_id=address_id
    )
