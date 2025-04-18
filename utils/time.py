from datetime import datetime, timedelta


def get_french_time_str():
    utc_now = datetime.utcnow()
    fr_time = utc_now + timedelta(hours=2)
    return fr_time.strftime("%d/%m/%Y %H:%M:%S")


def get_french_datetime():
    utc_now = datetime.utcnow()
    return utc_now + timedelta(hours=2)


def get_french_time_str():
    return (datetime.utcnow() + timedelta(hours=2)).strftime("%d/%m/%Y %H:%M:%S")


def get_french_datetime():
    return datetime.utcnow() + timedelta(hours=2)
