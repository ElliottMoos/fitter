import logging
from alembic.config import Config
from alembic import command

from app.core.settings import settings

logger = logging.getLogger(__name__)


def migrate(revision: str = "head") -> None:
    logger.info(f"Running migrations for revision: {revision}")
    config = Config(file_="/fitter/app/alembic.ini")
    config.set_main_option("script_location", "/fitter/app/migrations")
    config.set_main_option("sqlalchemy.url", settings.DB_URL)

    command.upgrade(config=config, revision=revision)


def main():
    migrate()


if __name__ == "__main__":
    main()
