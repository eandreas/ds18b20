import pandas as pd
import numpy as np
from pathlib2 import Path
from datetime import timedelta, datetime as dt

DEFAULT_PI_PATH = Path('/home/pi/get_temp_C.out')
FALLBACK_PATH = Path(
    '/Users/eandreas/projects/dev/ds18b20/webapp3/data/get_temp_C.out')


def convert_time(s):
    return s[0:5]


def load_data():
    path = DEFAULT_PI_PATH
    if not path.is_file():
        path = FALLBACK_PATH
    df = pd.read_csv(path, sep=' ', header=None, names=[
                     'dev_sn', 'date', 'time', 'temp_raw', 'temp_C'])

    # keep only values of the last 7 days
    now = dt.now()
    now = dt(now.year, now.month, now.day, now.hour,
             now.minute)  # date, hours and minutes only
    td7 = timedelta(days=7)
    one_week_ago = now - td7
    df = df[df.date >= one_week_ago.strftime('%Y-%m-%d')]

    # remove rows with nan entries
    df = df[~df.isna().any(axis=1)]

    # keep hour and minute from time only
    df['time'] = df['time'].apply(convert_time)

    # add a datetime column from date and time columns, drop the later ones
    df['date_time'] = pd.to_datetime(
        df['date']+df['time'], format='%Y-%m-%d%H:%M')
    df = df.drop(['date', 'time'], axis=1)

    dfs = {}
    idx = pd.date_range(start=one_week_ago, end=now, freq='T')

    for sn in df[df.temp_raw.notna()].dev_sn.unique():
        # create a copy for each device / serial number
        dfd = df[df.dev_sn == sn].copy()
        # reset index due to skipped rows (different serial number)
        dfd = dfd.reset_index(drop=True)
        # remov duplicate rows for the same time stamp
        dfd = dfd[~dfd.date_time.duplicated(keep='first')]
        # fill gaps in case of missing measured data points, use df to do ut everywhere the same way
        dfd = dfd.set_index('date_time').reindex(
            idx).rename_axis('date_time').reset_index()
        # add a timestamp column
        dfd['timestamp'] = (dfd.date_time.values.astype(
            np.int64) // 10 ** 9).tolist()
        # store within dictionary
        dfs.update({sn: dfd})
    return dfs
