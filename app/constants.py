import datetime as dt
import time

TWEPOCH_DATETIME = dt.datetime(2010, 1, 10, 3, 14, 20, 25)


TWEPOCH = int(round(time.mktime(TWEPOCH_DATETIME.timetuple()) * 1000))
