from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.core.settings import settings
from app.core import tasks
from app.api.routes import api_router, template_router
from app.models import FitterRead
from app.api.dependencies.auth import get_fitter_from_session_token


def get_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.mount("/static", StaticFiles(directory="app/api/static"), name="static")

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router)
    app.include_router(template_router)

    return app


app = get_application()
templates = Jinja2Templates(directory="app/api/templates")


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    active_fitter: FitterRead = Depends(get_fitter_from_session_token),
):
    if active_fitter:
        return templates.TemplateResponse(
            "index.html",
            {
                "title": "Fittr - Home",
                "request": request,
                "active_fitter": active_fitter,
            },
        )
    return RedirectResponse("/login")
