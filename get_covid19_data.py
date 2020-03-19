# https://dev.socrata.com/foundry/data.cdc.gov/x8jf-txib
# requests.get("https://data.cdc.gov/resource/x8jf-txib.json")

import datetime
import io
import logging
import os

import pandas as pd
import requests

logging.basicConfig(level=logging.DEBUG)


def _get_date_range():
    start_date = datetime.datetime(2020, 1, 22)
    today_date = datetime.datetime.today()
    time_delta = today_date - start_date
    logging.debug(f"time from start date: {time_delta.days} days")
    date_range = []
    for dt in range(0, time_delta.days):
        result = start_date + datetime.timedelta(days=dt)
        date_range.append(result.strftime("%m-%d-%Y"))
    return date_range


def _get_csv_data(date, filename):
    url = f'https://raw.github.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date}.csv'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as ex:
        logging.debug(
            f"request to pull {date} data failed - response: {response.content} status_code: {response.status_code}")
        raise ex
    content = response.content
    csv_data = pd.read_csv(io.StringIO(content.decode('utf-8')))
    csv_data.to_csv(filename)


def _get_jhopkins_data(date_range):
    for dt in date_range:
        filename = f"data/{dt}.csv"
        if not os.path.exists(filename):
            logging.debug(f"downloading csv for date: {dt}")
            _get_csv_data(date=dt, filename=filename)


data_dt_range = _get_date_range()
_get_jhopkins_data(data_dt_range)
