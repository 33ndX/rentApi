
from datetime import datetime


def serialize_datetime(date: datetime) -> str | None:
    """Serialize datetime to YYYY-MM-DD HH:MM:SS format."""
    if date is None:
        return None
    return date.strftime("%Y-%m-%d %H:%M:%S")
