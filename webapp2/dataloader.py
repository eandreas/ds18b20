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
            self.__figs = {}
            self.__last_fig_id = 'fig_12h'
            self.__n = {
                'fig_1h': 60,
                'fig_3h': 3 * 60,
                'fig_6h': 6 * 60,
                'fig_12h': 12 * 60,
                'fig_1d': 24 * 60,
                'fig_7d': 7 * 24 * 60,
                'fig_30d': 30 * 24 * 60,
                'fig_1y': 365 * 24 * 60
            }

    def get_df(self):
        if self.__df_full is None:
            self.__df_full = self.load_data()
        return self.__df_full
    
    def get_last_fig_id(self):
        return self.__last_fig_id

    def set_last_fig_id(self, fig_id):
        self.__last_fig_id = fig_id
    
    def get_fig(self, fig_id):
        if fig_id == 'fig_all':
            return self.get_fig_all()
        if fig_id in self.__figs:
            return self.__figs[fig_id]
        n = min(len(self.__df_full), self.__n[fig_id])
        start = self.__df_full.date_time.values[-n]
        self.__figs[fig_id] = self.__serve_figure(self.__compress_df(start))
        return self.__figs[fig_id]
    
    def get_fig_all(self):
        if 'fig_all' in self.__figs:
            return self.__figs['fig_all']
        start = self.__df_full.date_time.values[0]
        self.__figs['fig_all'] = self.__serve_figure(self.__compress_df(start))
        return self.__figs['fig_all']

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
            df = df.iloc[::-n]
        return df
    
    def __serve_figure(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(df.date_time),
            y=list(df.temp_C),
            name='t_corr',
            line=dict(color='skyblue', width=3, dash='solid')
        ))
        fig.add_trace(go.Scatter(
            x=list(df.date_time),
            y=list(df.temp_raw),
            name='t_raw',
            line=dict(color='darkgray', width=1, dash='dot')
        ))
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
        self.__figs = {}

    def get_current_C(self):
        return format(self.__df_full['temp_C'].values[-1], '.1f')

    def get_latest_datetime(self, n = 1):
        return pd.to_datetime(self.__df_full['date_time'].values[-n])

    def get_average_C(self, fig_id):
        n = min(len(self.__df_full), self.__n[fig_id])
        start = pd.to_datetime(self.__df_full.date_time.values[-n])
        df = self.__df_full[self.__df_full.date_time >= start]
        #print(f'len(self.__df_full)={len(self.__df_full)}, len(df)={len(df)}')
        end = pd.to_datetime(self.__df_full.date_time.values[-1])
        #print(f'get_average: start.date={start.date()}, end.date={end.date()}')
        return df['temp_C'].mean(), start, end

    def get_tendency(self, delta_prev = 0.1, delta_mean = 0.06):
        ct = self.__df_full['temp_C'].values[-1]
        pt = self.__df_full.tail(2).head(1)['temp_C'].values[-1]
        at = self.__df_full.tail(5).head(4)['temp_C'].mean()
        if ct > pt + delta_prev or ct > (at + delta_mean):
            return "steigend"
        elif ct < pt - delta_prev  or ct < (at - delta_mean):
            return "sinkend"
        else:
            return "stabil"
    
