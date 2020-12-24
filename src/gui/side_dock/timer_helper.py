from typing import Tuple

import pytz
import time

from datetime import datetime, timedelta


def get_tasks_countdowns() -> Tuple[datetime, datetime, float, float]:
    """
    returns [UTC+8 Time (in format), Local Time (in format), next daily (in sec), next weekly (in sec)]
    """
    utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
    cn_time = utc_time.astimezone(pytz.timezone('Asia/Shanghai'))
    local_time = utc_time.astimezone()

    def datetime_to_unixtime(t: datetime) -> float:
        return time.mktime(t.timetuple())

    if cn_time.hour < 3:
        next_daily = datetime(cn_time.year, cn_time.month, cn_time.day, 3, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    else:
        tmr = cn_time + timedelta(days=1)
        next_daily = datetime(tmr.year, tmr.month, tmr.day, 3, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    next_daily_diff = datetime_to_unixtime(next_daily) - datetime_to_unixtime(cn_time)

    if cn_time.hour < 4:
        next_weekly = datetime(cn_time.year, cn_time.month, cn_time.day, 4, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    else:
        next_weekly = datetime(cn_time.year, cn_time.month, cn_time.day, 4, 0, 0, 0,
                               tzinfo=pytz.timezone('Asia/Shanghai'))
        days_diff = timedelta(days=-cn_time.weekday(), weeks=1).days
        next_weekly += timedelta(days=days_diff)
    next_year = datetime(year=cn_time.year + 1, month=1, day=1, tzinfo=pytz.timezone('Asia/Shanghai'))
    diff1 = datetime_to_unixtime(next_weekly) - datetime_to_unixtime(cn_time)
    diff2 = datetime_to_unixtime(next_year) - datetime_to_unixtime(cn_time)
    next_weekly_diff = min(diff1, diff2)
    return cn_time, local_time, next_daily_diff, next_weekly_diff


def _calc_left_time(t) -> int:
    _diff = t - int(time.time())
    return 0 if _diff <= 0 else _diff
