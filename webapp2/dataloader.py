from pathlib2 import Path
import pandas as pd

DEFAULT_PI_PATH = Path('/home/pi/get_temp_C.out')
FALLBACK_PATH = Path('/Users/eandreas/projects/dev/ds18b20/webapp2/data/get_temp_C.out')

def load_data(path = DEFAULT_PI_PATH, fallback_path = FALLBACK_PATH, caller="unknown"):
    if not path.is_file():
        path = fallback_path
    print(f'Reading data from {path}, caller={caller}')
    df = pd.read_csv(path, sep=' ', header=None, names=['dev_sn', 'date', 'time', 'temp_raw', 'temp_C'], parse_dates=[['date', 'time']])
    print(f'df starts at {df.date_time.values[0]} and ends at {df.date_time.values[-1]}')
    return df