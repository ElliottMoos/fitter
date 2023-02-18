from fastapi import FastAPI, Request, Depends
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.core.settings import settings
from app.core import tasks
from app.server.routes import api_router, template_router
from app.models import FitterRead
from app.server.dependencies.auth import (
    active_fitter,
    RequiresLoginException,
)


def get_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.mount("/static", StaticFiles(directory="app/server/static"), name="static")

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router)
    app.include_router(template_router)

    return app


app = get_application()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Handle unauthorized user requests
@app.exception_handler(RequiresLoginException)
async def unauthorized_user_handler(
    request: Request, exc: RequiresLoginException
) -> Response:
    return RedirectResponse(url="/login")


templates = Jinja2Templates(directory="app/server/templates")


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    active_fitter: FitterRead = Depends(active_fitter),
):
    return templates.TemplateResponse(
        "index.html",
        {
            "title": "Fittr - Fittings",
            "request": request,
            "active_fitter": active_fitter,
        },
    )
