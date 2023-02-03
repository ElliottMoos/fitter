from fastapi import APIRouter

from app.api.routes.addresses import addresses_router

router = APIRouter()

router.include_router(addresses_router)
