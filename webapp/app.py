import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

import pandas as pd
from pathlib2 import Path

def load_data():
    #temp_file = Path('../resources/get_temp.out')
    temp_file = Path('/home/pi/get_temp.out')
    return pd.read_csv(temp_file, sep=' ', header = None, names = ['date', 'time', 'temp'], parse_dates=[['date', 'time']])

def build_figure():
    df = load_data()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(df.date_time), y=list(df.temp)))
    fig.update_layout(
        title_text="Gemessene Temperatur - DS18B20@dragonfly",
        xaxis_title="Datum",
        yaxis_title="Temperatur / °C",
    )
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1 h",
                         step="hour",
                         stepmode="backward"),
                    dict(count=6,
                         label="6 h",
                         step="hour",
                         stepmode="backward"),
                    dict(count=1,
                         label="1 d",
                         step="day",
                         stepmode="backward"),
                    dict(count=7,
                         label="7 d",
                         step="day",
                         stepmode="backward"),
                    dict(count=1,
                         label="1 m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="1 y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig

def serve_layout():
    return html.Div(children=[
        html.H2(children='Raspberry Pi Temperaturmessung'),
        dcc.Graph(
            id='example-graph',
            figure=build_figure()
        )
    ])

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port = 8080)