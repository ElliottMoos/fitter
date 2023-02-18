from fastapi import Request, APIRouter, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services import auth_service
from app.db.repositories.fitter import FitterRepository
from app.server.dependencies.database import get_repository


login_router = APIRouter(prefix="/login", tags=["login"])
templates = Jinja2Templates(directory="app/server/templates")


@login_router.get("", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@login_router.post("")
async def login(
    request: Request,
    username: str = Form(),
    password: str = Form(),
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
):
    fitter = fitter_repo.get_fitter_by_username(username)

    if not fitter:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "title": "Fittr - Login", "error": "Unknown username"},
        )

    if auth_service.verify_password(password, fitter.password):
        session_token = auth_service.generate_session_token(fitter)
        response = RedirectResponse("/", status_code=303)
        response.set_cookie("session_token", session_token)
        return response

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "title": "Fittr - Login", "error": "Invalid credentials"},
    )
