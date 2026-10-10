from datetime import date


def parse_date(value):
    """Return the calendar date of an ISO date or timestamp."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return date.fromisoformat(value.strip())
