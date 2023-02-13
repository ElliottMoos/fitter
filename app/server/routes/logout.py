from fastapi import APIRouter
from fastapi.responses import RedirectResponse


logout_router = APIRouter(prefix="/logout", tags=["logout"])


@logout_router.get("")
async def logout():
    response = RedirectResponse("/login")
    response.delete_cookie("session_token")
    return response
