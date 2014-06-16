import calendar
import datetime

def javascript_timestamp(date, granularity):

    if granularity == 'day':
        date_format = '%Y-%m-%d'
    elif granularity == 'month':
        date_format = '%Y%m'
    elif granularity == 'year':
        date_format = '%Y'

    dt = datetime.datetime.strptime(date, date_format)
    """Multiply by 1000 for flot. Flot time series data is
    based on javascript timestamps, that is milliseconds,
    since January 1, 1970 00:00:00 UTC"""
    return calendar.timegm(dt.timetuple()) * 1000

def convert_jsts(jsts, granularity):
    dt = datetime.datetime.fromtimestamp(float(jsts)/1000) + datetime.timedelta(days=1)
    date = str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day)

    if granularity == 'day':
        start_date = date
        end_date = date
        date_range = (start_date, end_date)
    elif granularity == 'month':
        start_date = date
        days_in_month = calendar.monthrange(dt.year, dt.month)[1]
        end_dt = dt + datetime.timedelta(days = days_in_month - 1)
        end_date = str(end_dt.year) + '-' + str(end_dt.month) + '-' + str(end_dt.day)
        date_range = (start_date, end_date)
    elif granularity == 'year':
        start_date = date
        end_date = str(dt.year) + '-' + str(12) + '-' + str(31)
        date_range = (start_date, end_date)

    return date_range


