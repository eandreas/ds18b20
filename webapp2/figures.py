import plotly.graph_objects as go

# -- MOVE TO UTIL ?
import pandas as pd

def npdt2dtdt(npdt):
    return pd.Timestamp(npdt).to_pydatetime()
# -- end of MOVE TO UTIL


def build_figure(df, n = None):
    if n is not None:
        n = min(len(df), n)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(df.date_time), y=list(df.temp_C), name='t_corr'))
    fig.add_trace(go.Scatter(x=list(df.date_time), y=list(df.temp_raw), name='t_raw'))
    fig.update_layout(
        #title_text="Gemessene Temperatur - DS18B20@dragonfly",
        xaxis_title="Datum",
        yaxis_title="Temperatur / °C",
        template='none'
    )
    fig.update_layout(
        margin = dict(
            #l=50,
            #r=50,
            #b = 20,
            t = 10,
            pad=4
        ),
    )
    
    if n is not None:
        fig.update_layout(
            xaxis_range = [npdt2dtdt(df.date_time.values[-n]), npdt2dtdt(df.date_time.values[-1])]
        )

    return fig