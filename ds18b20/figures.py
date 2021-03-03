# AUTOGENERATED! DO NOT EDIT! File to edit: 02_figures.ipynb (unless otherwise specified).

__all__ = ['new_x_y', 'add_trace', 'get_figure']

# Cell
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import interp1d
import pandas as pd
from pathlib2 import Path
import datetime

# Cell
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

# Cell
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

# Cell
def get_figure(x, y, n, sz1, sz2, cs, cmin, cmax, convert_ts=False):
    x_new, y_new = new_x_y(x, y, n)
    if convert_ts:
        x = pd.to_datetime(x, unit='s')
        x_new = pd.to_datetime(x_new, unit='s')
    fig = go.Figure()
    add_trace(fig, x_new, y_new, sz1, cs, cmin, cmax, hi='skip', sl=False)
    add_trace(fig, x, y, sz2, cs, cmin, cmax, sl=False)
    return fig