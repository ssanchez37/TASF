import datetime as dt
import math


def excel_date(date1):
    if isinstance(date1, dt.datetime):
        temp = dt.datetime(1899, 12, 30)
        delta = date1 - temp
        return (float(delta.days) + (float(delta.seconds) / 86400) - 1) * 24
    elif isinstance(date1, dt.time):
        return int(date1.hour) + int(date1.minute) / 60 + int(date1.second) / 60
    else:
        return float(0.0)


def min2hour(mins):
    hoursdec = mins/60
    hours = math.floor(hoursdec)
    minsdec = hoursdec - hours
    mins = round(minsdec * 60)
    return hours, mins
