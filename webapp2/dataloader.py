from pathlib2 import Path
import pandas as pd
import plotly.graph_objects as go

class DataProviderSingleton:

    __instance = None
    __DEFAULT_PI_PATH = Path('/home/pi/get_temp_C.out')
    __FALLBACK_PATH = Path('/Users/eandreas/projects/dev/ds18b20/webapp2/data/get_temp_C.out')

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
            self.__fig_1h = None
            self.__fig_3h = None
            self.__fig_6h = None
            self.__fig_12h = None
            self.__fig_1d = None
            self.__fig_7d = None
            self.__fig_30d = None
            self.__fig_1y = None
            self.__fig_all = None
    
    def get_df(self):
        if self.__df_full is None:
            self.__df_full = self.load_data()
        return self.__df_full

    def get_fig_1h(self):
        if self.__fig_1h is None:
            n = min(len(self.__df_full), 60)
            start = self.__df_full.date_time.values[-n]
            self.__fig_1h = self.__serve_figure(self.__compress_df(start))
        return self.__fig_1h
    
    def get_fig_3h(self):
        if self.__fig_3h is None:
            n = min(len(self.__df_full), 3 * 60)
            start = self.__df_full.date_time.values[-n]
            self.__fig_3h = self.__serve_figure(self.__compress_df(start))
        return self.__fig_3h
    
    def get_fig_6h(self):
        if self.__fig_6h is None:
            n = min(len(self.__df_full), 6 * 60)
            start = self.__df_full.date_time.values[-n]
            self.__fig_6h = self.__serve_figure(self.__compress_df(start))
        return self.__fig_6h
    
    def get_fig_12h(self):
        if self.__fig_12h is None:
            n = min(len(self.__df_full), 12 * 60)
            start = self.__df_full.date_time.values[-n]
            self.__fig_12h = self.__serve_figure(self.__compress_df(start))
        return self.__fig_12h

    def get_fig_1d(self):
        if self.__fig_1d is None:
            n = min(len(self.__df_full), 24 * 60)
            start = self.__df_full.date_time.values[-n]
            self.__fig_1d = self.__serve_figure(self.__compress_df(start))
        return self.__fig_1d
    
    def get_fig_7d(self):
        if self.__fig_7d is None:
            n = min(len(self.__df_full), 7 * 24 * 60)
            start = self.__df_full.date_time.values[-n]
            self.__fig_7d = self.__serve_figure(self.__compress_df(start))
        return self.__fig_7d
    
    def get_fig_30d(self):
        if self.__fig_30d is None:
            n = min(len(self.__df_full), 30 * 24 * 60)
            start = self.__df_full.date_time.values[-n]
            self.__fig_30d = self.__serve_figure(self.__compress_df(start))
        return self.__fig_30d

    def get_fig_1y(self):
        if self.__fig_1y is None:
            n = min(len(self.__df_full), 365 * 24 * 60)
            start = self.__df_full.date_time.values[-n]
            self.__fig_1y = self.__serve_figure(self.__compress_df(start))
        return self.__fig_1y
    
    def get_fig_all(self):
        if self.__fig_all is None:
            start = self.__df_full.date_time.values[0]
            self.__fig_all = self.__serve_figure(self.__compress_df(start))
        return self.__fig_all

    def load_data(self):
        path = self.__DEFAULT_PI_PATH
        if not path.is_file():
            path = self.__FALLBACK_PATH
        names = ['dev_sn', 'date', 'time', 'temp_raw', 'temp_C']
        self.__df_full = pd.read_csv(path, sep=' ', header=None, names = names, parse_dates=[['date', 'time']])
    
    def __compress_df(self, start, res = 200):
        df = self.__df_full[self.__df_full.date_time >= start]
        if len(df) >= 2 * res:
            n = int(len(df) / res)
            df = df.iloc[::n, :]
        return df
    
    def __serve_figure(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(df.date_time), y=list(df.temp_C), name='t_corr'))
        fig.add_trace(go.Scatter(x=list(df.date_time), y=list(df.temp_raw), name='t_raw'))
        fig.update_layout(
            xaxis_title="Datum",
            yaxis_title="Temperatur / °C",
            template='none',
            margin = dict(
                t = 10,
                pad=4
            ),
        )
        return fig
    
    def clear_figures(self):
        self.__fig_1h = None
        self.__fig_3h = None
        self.__fig_6h = None
        self.__fig_12h = None
        self.__fig_1d = None
        self.__fig_7d = None
        self.__fig_30d = None
        self.__fig_1y = None
        self.__fig_all = None

    def get_current_C(self):
        return format(self.__df_full['temp_C'].values[-1], '.1f')

    def get_latest_datetime(self, n = 1):
        return pd.to_datetime(self.__df_full['date_time'].values[-n])
    
