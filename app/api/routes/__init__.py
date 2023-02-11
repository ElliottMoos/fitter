from fastapi import APIRouter

from app.api.routes.addresses import addresses_router
from app.api.routes.customers import customers_router
from app.api.routes.fitters import fitters_router
from app.api.routes.fittings import fittings_router
from app.api.routes.login import login_router
from app.api.routes.logout import logout_router
from app.api.routes.stores import stores_router

api_router = APIRouter(prefix="/api")

api_router.include_router(addresses_router)
api_router.include_router(customers_router)
api_router.include_router(fitters_router)
api_router.include_router(fittings_router)
api_router.include_router(stores_router)

template_router = APIRouter(prefix="")
template_router.include_router(login_router)
template_router.include_router(logout_router)
