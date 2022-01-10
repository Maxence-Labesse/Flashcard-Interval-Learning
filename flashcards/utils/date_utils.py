"""This module provides functions compare 2 dates (without time)

test_same_dates:
    compare 2 dates
to_datetime_date:
    transform string or datetime.datetime to datetime.date
"""
import datetime


def test_same_dates(date1, date2):
    """Process 2 dates to datetime.date format and compare them

    Parameters
    ----------
    date1: str, datetime.datetime or datetime.date

    date2: str, datetime.datetime or datetime.date

    Returns
    -------
    bool:
        True if the 2 dates are the same, False otherwise

    """
    date1 = to_datetime_date(date1)
    date2 = to_datetime_date(date2)

    return date1 == date2


def to_datetime_date(date):
    """transform date to datetime.date format.

    If the format is already datetime.date, just
    return the date

    Parameters
    ----------
    date: str, datetime.datetime or datetime.
        date to transform
    Returns
    -------
    datetime.date:
        processed date
    """

    assert (type(date) in [str, datetime.datetime, datetime.date])

    if isinstance(date, str):
        processed_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    elif isinstance(date, datetime.datetime):
        processed_date = date.date()
    else:
        processed_date = date

    return processed_date
