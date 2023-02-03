from fastapi import FastAPI

from app.core.settings import settings
from app.core import tasks

from app.api.routes import router as api_router


def get_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()


@app.get("/")
async def root():
    return {"message": "Hello World"}
