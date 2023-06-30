from datetime import datetime


def isoparse(value: str) -> datetime:
    # Python <3.11 doesn't fully support parsing ISO8601 datetime strings. This
    # workaround replaces the ending `Z` or `z` with `+00:00` and allows
    # `datetime.fromisoformat` to parse the datetime string.
    if value[-1] in "Zz":
        value = value[:-1] + "+00:00"

    return datetime.fromisoformat(value)
