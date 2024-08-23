import datetime


def to_datetime(value):
    if isinstance(value, datetime.datetime):
        return value

    if isinstance(value, float) or isinstance(value, int):
        return datetime.datetime.fromtimestamp(value)

    if not isinstance(value, str):
        raise TypeError(f"Unsupported type: {type(value)}")

    try:
        return datetime.datetime.fromisoformat(value)
    except ValueError:
        return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def format_date(value: datetime.datetime, format="%b %d, %Y %I:%M:%S %p"):
    datetime_obj = to_datetime(value)
    return datetime_obj.strftime(format)


def add_to_datetime(
    start_datetime: datetime.datetime = None,
    microseconds: float = 0,
    milliseconds: float = 0,
    seconds: float = 0,
    minutes: float = 0,
    hours: float = 0,
    days: float = 0,
    weeks: float = 0,
):
    return (start_datetime or datetime.datetime.now()) + datetime.timedelta(
        microseconds=microseconds,
        milliseconds=milliseconds,
        seconds=seconds,
        minutes=minutes,
        hours=hours,
        days=days,
        weeks=weeks,
    )


def is_in_future(value):
    return to_datetime(value) > datetime.datetime.now()


def get_duration(delta: datetime.timedelta):
    return str(delta).split(".")[0]
