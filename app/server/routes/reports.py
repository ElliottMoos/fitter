from datetime import date, datetime
from typing import Optional, List, Dict
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.server.dependencies.pagination import Paginator, get_paginator
from app.server.dependencies.database import get_repository
from app.server.dependencies.auth import active_fitter
from app.db.repositories.fitting import FittingRepository
from app.db.repositories.fitter import FitterRepository
from app.models import FittingReadAllRelations, FitterRead


reports_api_router = APIRouter(prefix="/reports", tags=["reports"])
reports_template_router = APIRouter(prefix="/reports", tags=["reports"])
templates = Jinja2Templates(directory="app/server/templates")


@reports_api_router.get("/fittings-today", name="reports:fitting-today")
async def fittings_today(
    *,
    today: Optional[date] = Query(default=date.today()),
    fitting_repo: FittingRepository = Depends(get_repository(FittingRepository)),
) -> Dict[str, int]:
    today_start = datetime(today.year, today.month, today.day)
    today_end = datetime(today.year, today.month, today.day, 23)
    fittings = {
        "9AM": 0,
        "10AM": 0,
        "11AM": 0,
        "12PM": 0,
        "1PM": 0,
        "2PM": 0,
        "3PM": 0,
        "4PM": 0,
        "5PM": 0,
        "6PM": 0,
    }
    for fitting in fitting_repo.get_fittings_start_end(today_start, today_end):
        fittings[fitting.start.strftime("%-I%p")] += 1
    return fittings


@reports_api_router.get("/fittings-by-fitter", name="reports:fittings-by-fitter")
async def fittings_by_fitter(
    *,
    fitter_repo: FitterRepository = Depends(get_repository(FitterRepository)),
    fitting_repo: FittingRepository = Depends(get_repository(FittingRepository)),
) -> Dict[str, int]:
    return {
        f"{fitter.first_name} {fitter.last_name}": len(
            fitting_repo.get_fittings_for_fitter(fitter_id=fitter.id)
        )
        for fitter in fitter_repo.get_all_fitters()
    }


@reports_template_router.get("/fitting-search", name="reports:fitting-search")
async def fitting_search_page(
    *,
    request: Request,
    start_date: Optional[date] = Query(default=None),
    end_date: Optional[date] = Query(default=None),
    paginator: Paginator[FittingReadAllRelations] = Depends(
        get_paginator(FittingReadAllRelations)
    ),
    fitting_repo: FittingRepository = Depends(get_repository(FittingRepository)),
    active_fitter: FitterRead = Depends(active_fitter),
):
    page = None

    if start_date and end_date:
        page = paginator.paginate(
            fitting_repo.get_fittings_start_end(
                start=datetime(start_date.year, start_date.month, start_date.day),
                end=datetime(end_date.year, end_date.month, end_date.day, 23),
            )
        )
    elif start_date and not end_date:
        page = paginator.paginate(
            fitting_repo.get_fittings_start(
                start=datetime(start_date.year, start_date.month, start_date.day)
            )
        )
    elif end_date and not start_date:
        page = paginator.paginate(
            fitting_repo.get_fittings_end(
                end=datetime(end_date.year, end_date.month, end_date.day, 23)
            )
        )
    else:
        page = paginator.paginate(fitting_repo.get_all_fittings())
    return templates.TemplateResponse(
        "fitting-search.html",
        {
            "title": "Fittr - Reports",
            "request": request,
            "page": page,
            "active_fitter": active_fitter,
            "start_date_query": f"&start_date={start_date}" if start_date else None,
            "end_date_query": f"&end_date={end_date}" if end_date else None,
        },
    )


@reports_template_router.get("/fittings-today", name="reports:fittings-today")
async def fittings_today_page(
    *,
    request: Request,
    active_fitter: FitterRead = Depends(active_fitter),
):
    return templates.TemplateResponse(
        "fittings-today.html",
        {
            "title": "Fittr - Reports",
            "request": request,
            "active_fitter": active_fitter,
        },
    )


@reports_template_router.get("/fittings-by-fitter", name="reports:fittings-by-fitter")
async def fittings_by_fitter_page(
    *,
    request: Request,
    active_fitter: FitterRead = Depends(active_fitter),
):
    return templates.TemplateResponse(
        "fittings-by-fitter.html",
        {
            "title": "Fittr - Reports",
            "request": request,
            "active_fitter": active_fitter,
        },
    )
