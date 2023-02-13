import logging

from tenacity import retry, after_log, before_log, stop_after_attempt, wait_fixed
from sqlmodel import create_engine, Session

from app.core.settings import settings

logger = logging.getLogger(__name__)
max_tries = 60 * 5
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def check_connection() -> None:
    try:
        engine = create_engine(settings.DB_URL)
        session = Session(engine)
        session.exec("SELECT 1")
    except Exception as exc:
        logger.error(exc)
        raise exc


def main() -> None:
    logger.info("Checking db connection")
    check_connection()
    logger.info("Finished db connection check")


if __name__ == "__main__":
    main()
