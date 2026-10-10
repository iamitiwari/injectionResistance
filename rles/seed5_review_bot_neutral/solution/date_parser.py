from datetime import date, datetime


def parse_date(value):
    """Return the calendar date of an ISO date or timestamp."""
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    text = value.strip()
    if "T" in text:
        return datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text).date()
    return date.fromisoformat(text)
