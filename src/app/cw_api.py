from apikey import _API_KEY
import requests
import json
from date_convert import javascript_timestamp, convert_jsts
import datetime

def cw_search_text(keywords, date_low, date_high, granularity):
    API_KEY = _API_KEY
    api_results = []

    date = convert_jsts(date_low, granularity)
    for keyword in keywords:
        if keyword != '':
            query_params = {'apikey': API_KEY,
                        'phrase': keyword,
                        'start_date': date[0],
                        'end_date': date[1],
                        'sort': 'date desc',
                        'per_page': 5
                        }

            endpoint = 'http://capitolwords.org/api/1/text.json'

            response = requests.get(endpoint, params=query_params)
            if response.status_code == 200:
                results = json.loads(response.text)
                api_results.append(results)

    return api_results

def cw_search_keywords(keywords, date_low, date_high, granularity):
    API_KEY = _API_KEY
    api_results = []
    for keyword in keywords:
        query_params = {'apikey': API_KEY,
                    'phrase': keyword,
                    'start_date': date_low,
                    'end_date': date_high,
                    'granularity': granularity
                    }

        endpoint = 'http://capitolwords.org/api/dates.json'

        response = requests.get(endpoint, params=query_params)
        if response.status_code == 200:
            results = json.loads(response.text)
            if granularity == 'day':
                results_entire_range = add_all(date_low, date_high, results, granularity="day")
                for result in results_entire_range['results']:
                    result['day'] = javascript_timestamp(result['day'], granularity)
            elif granularity == 'month':
                results_entire_range = add_all(date_low, date_high, results, granularity="month")
                for result in results_entire_range['results']:
                    result['month'] = javascript_timestamp(result['month'], granularity)
            elif granularity == 'year':
                results_entire_range = add_all(date_low, date_high, results, granularity="year")
                for result in results_entire_range['results']:
                    result['year'] = javascript_timestamp(result['year'], granularity)
            api_results.append(results)


    return api_results

def add_all(start_date, end_date, result, granularity):

    '''Function is used to add days with no results back into the list of results
       so that the graph will plot a point of 0 for that day.'''

    if granularity == 'day':
        date_format = '%Y-%m-%d'
    elif granularity == 'month':
        date_format = '%Y%m'
    elif granularity == 'year':
        date_format = '%Y'

    date_low = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    date_high = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    returned_dates = []
    for i in result['results']:
       returned_dates.append(datetime.datetime.strptime(i[granularity], date_format))
    if granularity == 'day':
        for i in range((date_high - date_low).days + 1):
            date =  date_low + datetime.timedelta(i)
            date_string = date.strftime(date_format)
            if date not in returned_dates:
                no_result = {"count": 0,
                                    granularity: date_string,
                                    }
                result['results'].insert(i, no_result)

    elif granularity == 'month':
        ym_start= 12*date_low.year + date_low.month - 1
        ym_end= 12*date_high.year + date_high.month - 1
        for ym in range( ym_start, ym_end + 1):
            y, m = divmod( ym, 12 )
            date = datetime.datetime(y, m + 1, 1)
            date_string = date.strftime(date_format)
            if date not in returned_dates:
                no_result = {"count": 0,
                                    granularity: date_string,
                                    }
                result['results'].insert(ym - ym_start, no_result)

    elif granularity == 'year':
        year_start = date_low.year
        year_end = date_high.year
        for year in range(year_start, year_end):
            date = datetime.datetime(year, 1, 1)
            date_string = date.strftime(date_format)
            if date not in returned_dates:
                no_result = {"count": 0,
                                    granularity: date_string,
                                    }
                result['results'].insert(year - year_start, no_result)

    return result
