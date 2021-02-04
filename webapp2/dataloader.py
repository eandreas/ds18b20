from pathlib2 import Path
import pandas as pd

DEFAULT_PI_PATH = Path('/home/pi/get_temp_C.out')
FALLBACK_PATH = Path('/Users/eandreas/projects/dev/ds18b20/webapp2/data/get_temp_C.out')

def load_data(path = DEFAULT_PI_PATH, fallback_path = FALLBACK_PATH):
    if not path.is_file():
        path = fallback_path
    df = pd.read_csv(path, sep=' ', header=None, names=['dev_sn', 'date', 'time', 'temp_raw', 'temp_C'], parse_dates=[['date', 'time']])
    return df

class DataProviderSingleton:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if DataProviderSingleton.__instance is None:
            DataProviderSingleton()
        return DataProviderSingleton.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if DataProviderSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DataProviderSingleton.__instance = self
            self.__df_full = None
    
    def get_df(self):
        if self.__df_full is None:
            self.__df_full = load_data(caller='get_df')
        return self.__df_full
    
    def set_df(self, df):
        self.__df_full = df