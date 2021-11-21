from datetime import datetime
from dateutil import tz


def timestamp_converter(hour_to_convert):
    hour = datetime.strptime(
        datetime.utcfromtimestamp(hour_to_convert).strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S",
    )
    hour = hour.replace(tzinfo=tz.gettz("GMT"))

    return str(hour.astimezone(tz.gettz("America/Sao Paulo")))[:-6]


print(timestamp_converter(1563142473))
