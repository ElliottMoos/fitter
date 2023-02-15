from fastapi import APIRouter

from app.server.routes.addresses import addresses_router
from app.server.routes.customer_create import customer_create_router
from app.server.routes.customer_update import customer_update_router
from app.server.routes.customers import customers_api_router
from app.server.routes.customers import customers_template_router
from app.server.routes.fitter_create import fitter_create_router
from app.server.routes.fitter_update import fitter_update_router
from app.server.routes.fitters import fitters_api_router
from app.server.routes.fitters import fitters_template_router
from app.server.routes.fittings import fittings_router
from app.server.routes.login import login_router
from app.server.routes.logout import logout_router
from app.server.routes.reports import reports_api_router
from app.server.routes.reports import reports_template_router
from app.server.routes.store_create import store_create_router
from app.server.routes.store_update import store_update_router
from app.server.routes.stores import stores_api_router
from app.server.routes.stores import stores_template_router

api_router = APIRouter(prefix="/api")

api_router.include_router(addresses_router)
api_router.include_router(customers_api_router)
api_router.include_router(fitters_api_router)
api_router.include_router(fittings_router)
api_router.include_router(reports_api_router)
api_router.include_router(stores_api_router)

template_router = APIRouter(prefix="")
template_router.include_router(customer_create_router)
template_router.include_router(customer_update_router)
template_router.include_router(fitter_create_router)
template_router.include_router(fitter_update_router)
template_router.include_router(login_router)
template_router.include_router(logout_router)
template_router.include_router(reports_template_router)
template_router.include_router(customers_template_router)
template_router.include_router(fitters_template_router)
template_router.include_router(store_create_router)
template_router.include_router(store_update_router)
template_router.include_router(stores_template_router)
