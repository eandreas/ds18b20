import plotly.graph_objects as go
import numpy as np


def serve_figure():
    x = np.arange(10)
    fig = go.Figure(data=go.Scatter(x=x, y=x**2, mode='lines', line=dict(color='rgba(226, 240, 237, 0.5)', width=5)))
    fig.update_layout(
        autosize=True,
        # width=200,
        # height=100,
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