# -*- coding: utf-8 -*-
"""Utilities for Gregorian -> Jalali (Persian) date formatting and digit conversion"""

from datetime import datetime, timedelta

PERSIAN_DIGITS = {
    '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
    '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
}

# Afghanistan Standard Time is UTC+4:30
AFGHANISTAN_TIMEZONE_OFFSET = timedelta(hours=4, minutes=30)


def to_persian_digits(s):
    return ''.join(PERSIAN_DIGITS.get(ch, ch) for ch in str(s))


def gregorian_to_jalali(gy, gm, gd):
    # Algorithm from the Persian calendar conversion
    g_d_m = [0,31,59,90,120,151,181,212,243,273,304,334]
    if (gy > 1600):
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 365*gy + (gy2+3)//4 - (gy2+99)//100 + (gy2+399)//400 - 80 + gd + g_d_m[gm-1]
    jy += 33*(days//12053)
    days %= 12053
    jy += 4*(days//1461)
    days %= 1461
    if (days > 365):
        jy += (days-1)//365
        days = (days-1)%365
    if (days < 186):
        jm = 1 + days//31
        jd = 1 + days%31
    else:
        jm = 7 + (days-186)//30
        jd = 1 + (days-186)%30
    return jy, jm, jd


def format_datetime_to_persian(dt_str, persian_digits=True, include_time=True):
    """Convert a datetime string (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS) to Jalali date string.
    Adjusts time to Afghanistan timezone (UTC+4:30).
    Returns string like '۱۴۰۴/۱۱/۱۹ ۱۰:۲۳' (persian digits) or '1404/11/19 10:23'.
    """
    if not dt_str:
        return '-'
    
    parts = dt_str.split()
    date_part = parts[0]
    time_part = parts[1] if len(parts) > 1 else ''
    
    # Parse the UTC datetime
    y, m, d = [int(x) for x in date_part.split('-')]
    
    # If time is provided, adjust to Afghanistan timezone
    if include_time and time_part:
        h, min_val, sec_val = [int(x) for x in (time_part.split(':') + ['00'])[:3]]
        # Create UTC datetime
        utc_dt = datetime(y, m, d, h, min_val, sec_val)
        # Add Afghanistan timezone offset (UTC+4:30)
        local_dt = utc_dt + AFGHANISTAN_TIMEZONE_OFFSET
        y, m, d = local_dt.year, local_dt.month, local_dt.day
        h, min_val = local_dt.hour, local_dt.minute
    else:
        h = min_val = 0
    
    # Convert to Jalali
    jy, jm, jd = gregorian_to_jalali(y, m, d)
    
    if include_time and time_part:
        hhmm = f"{h:02d}:{min_val:02d}"
        res = f"{jy:04d}/{jm:02d}/{jd:02d} {hhmm}"
    else:
        res = f"{jy:04d}/{jm:02d}/{jd:02d}"
    
    if persian_digits:
        return to_persian_digits(res)
    return res
