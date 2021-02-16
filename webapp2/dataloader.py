from pathlib2 import Path
import pandas as pd
import plotly.graph_objects as go
from constants import graph_colors as gc
import numpy as np

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
            self.__dfs = None
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

    def get_dfs(self):
        if self.__dfs is None:
            self.load_data()
        return self.__dfs
    
    def get_last_fig_id(self):
        return self.__last_fig_id

    def set_last_fig_id(self, fig_id):
        self.__last_fig_id = fig_id
    
    def get_fig(self, fig_id):
        if fig_id == 'fig_all':
            return self.get_fig_all()
        if fig_id in self.__figs:
            return self.__figs[fig_id]
        sn0 = list(self.__dfs.keys())[0]
        n = min(len(self.__dfs[sn0]), self.__n[fig_id])
        start = self.__dfs[sn0].date_time.values[-n]
        self.__figs[fig_id] = self.__serve_figure(start)
        return self.__figs[fig_id]
    
    def get_fig_all(self):
        if 'fig_all' in self.__figs:
            return self.__figs['fig_all']
        start = self.__df_full.date_time.values[0]
        self.__figs['fig_all'] = self.__serve_figure(start)
        return self.__figs['fig_all']

    def load_data(self):
        path = self.__DEFAULT_PI_PATH
        if not path.is_file():
            path = self.__FALLBACK_PATH
        names = ['dev_sn', 'date', 'time', 'temp_raw', 'temp_C']
        df = pd.read_csv(path, sep=' ', header=None, names = names, parse_dates=[['date', 'time']])
        
        # keep only rows witout nan entries
        df = df[~df.isna().any(axis=1)]
        # keep only dates, hours, and minutes from date_time column
        df.date_time = df.date_time.dt.strftime('%Y-%m-%d %H:%M')
        df.date_time = pd.to_datetime(df['date_time'], format='%Y%m%d %H:%M')

        idx = pd.date_range(
            start = df.date_time.min().strftime('%Y-%m-%d %H:%M'),
            end = df.date_time.max().strftime('%Y-%m-%d %H:%M'),
            freq = 'T'
        )
    
        dfs = {}
    
        for sn in df[df.temp_raw.notna()].dev_sn.unique():
            # create a copy for each device / serial number
            dfd = df[df.dev_sn == sn].copy()
            # reset index due to skipped rows (different serial number)
            dfd = dfd.reset_index(drop = True)
            # remov duplicate rows for the same time stamp
            dfd = dfd[~dfd.date_time.duplicated(keep='first')]
            # fill gaps in case of missing measured data points, use df to do ut everywhere the same way
            dfd = dfd.set_index('date_time').reindex(idx).rename_axis('date_time').reset_index()
            # store within dictionary
            dfs.update({sn: dfd})
        self.__dfs = dfs
    
    def __compress_df(self, df, start, res = 200):
        df = df[df.date_time >= start]
        if len(df) >= 2 * res:
            n = int(len(df) / res)
            df = df.iloc[::-n]
        return df
    
    def __serve_figure(self, start):
        fig = go.Figure()
        i = 0
        for sn in self.__dfs.keys():
            df = self.__compress_df(self.__dfs[sn], start)
            fig.add_trace(go.Scatter(
                x=list(df.date_time),
                y=list(df.temp_C),
                name=sn,
                #line=dict(color='skyblue', width=2, dash='solid'),
                line=dict(color=gc[i], width=2, dash='solid'),
                #fill='tozeroy',
            ))
            #fig.add_trace(go.Scatter(
            #    x=list(df.date_time),
            #    y=list(df.temp_raw),
            #    name='t_raw',
            #    line=dict(color='darkgray', width=1, dash='dot')
            #))
            fig.update_layout(
                xaxis_title="Datum",
                yaxis_title="Temperatur / °C",
                template='none',
                #autosize=False,
                #width=1000,
                #height=500,
                margin = dict(
                    l = 80,
                    r = 10,
                    b = 0,
                    t = 0,
                    pad = 4
                ),
                legend = dict(
                    orientation = "h",
                    yanchor = "bottom",
                    y = -0.3,
                    xanchor = "right",
                    x = 1.0
                )
            )
            i += 1
        return fig
    
    def clear_figures(self):
        self.__figs = {}

    def get_current_C(self):
        t = list()
        for sn in self.__dfs.keys():
            t.append(self.__dfs[sn]['temp_C'].values[-1])
        return format(np.array(t, np.float).mean(), '.1f')

    def get_latest_datetime(self, n = 1):
        sn = list(self.__dfs.keys())[0]
        return pd.to_datetime(self.__dfs[sn]['date_time'].values[-n])

    def get_average_C(self, fig_id):
        n = min(len(self.__df_full), self.__n[fig_id])
        start = pd.to_datetime(self.__df_full.date_time.values[-n])
        df = self.__df_full[self.__df_full.date_time >= start]
        #print(f'len(self.__df_full)={len(self.__df_full)}, len(df)={len(df)}')
        end = pd.to_datetime(self.__df_full.date_time.values[-1])
        #print(f'get_average: start.date={start.date()}, end.date={end.date()}')
        return df['temp_C'].mean(), start, end

    def get_tendency(self, delta_prev = 0.1, delta_mean = 0.06, n = 10):
        t_now = self.__df_full.iloc[-1].temp_C
        t_prev = self.__df_full.iloc[-2].temp_C
        t_mean = self.__df_full.iloc[-(n+1):-1].temp_C.mean()
    
        if t_now > t_prev + delta_prev:
            return "steigend"
        elif t_now > t_mean + delta_mean:
            return "steigend"
        elif t_now < t_prev - delta_prev:
            return "sinkend"
        elif t_now < t_mean - delta_mean:
            return "sinkend"
        else:
            return "stabil"
    

    
