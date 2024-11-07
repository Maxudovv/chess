from kombu.exceptions import OperationalError

from config import celery_app


def is_celery_alive() -> bool:
    """Check celery worker availability."""

    try:
        return bool(celery_app.control.ping(limit=1))
    except OperationalError:
        return False
