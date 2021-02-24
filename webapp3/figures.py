import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

CS=[
    [0, "rgb(49,54,149)"],
    [0.1111111111111111, "rgb(69,117,180)"],
    [0.2222222222222222, "rgb(116,173,209)"],
    [0.3333333333333333, "rgb(171,217,233)"],
    [0.4444444444444444, "rgb(224,243,248)"],
    [0.5555555555555556, "rgb(254,224,144)"],
    [0.6666666666666666, "rgb(253,174,97)"],
    [0.7777777777777778, "rgb(244,109,67)"],
    [0.8888888888888888, "rgb(215,48,39)"],
    [1.0, "rgb(165,0,38)"]
]

def new_x_y(x, y, n, kind='linear'):
    """
    Returns an interpolation of type kind f with n data points based on y = f(x)
    
    x, y: arrays defining y = f(x)
    n: the number of interpolated date points returned
    kind: type of interpolation ('linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic',
    'previous', 'next', where 'zero', 'slinear', 'quadratic' and 'cubic')
    """
    f_x = interp1d(x, y)
    x_new = np.linspace(x[0], x[-1], n)
    y_new = f_x(x_new)
    return x_new, y_new

def add_trace(fig, x, y, sz, cs, cmin, cmax, hi=None, sl=True):
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker={
                'color': y,
                'cmin': cmin,
                'cmax': cmax,
            'colorscale': cs, 
            'size': sz,
        },
        hoverinfo=hi,
        showlegend=sl,
        )
    )

def get_figure(x, y, n, sz1, sz2, cs, cmin, cmax, convert_ts=False):
    x_new, y_new = new_x_y(x, y, n)
    if convert_ts:
        x = pd.to_datetime(x, unit='s')
        x_new = pd.to_datetime(x_new, unit='s')
    fig = go.Figure()
    add_trace(fig, x_new, y_new, sz1, cs, cmin, cmax, hi='skip', sl=False)
    add_trace(fig, x, y, sz2, cs, cmin, cmax, sl=False)
    fig.update_layout(
        autosize=True,
        #width=100,
        height=300,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        ),
        xaxis_visible=False,
        yaxis_visible=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

def serve_figure():
    x = np.arange(10)
    fig = go.Figure(data=go.Scatter(x=x, y=x**2, mode='lines', line=dict(color='rgba(226, 240, 237, 0.5)', width=5)))
    fig.update_layout(
        autosize=False,
        # width=200,
        height=100,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=4
        ),
        xaxis_visible=False,
        yaxis_visible=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig