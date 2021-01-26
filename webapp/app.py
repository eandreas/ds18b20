from pathlib2 import Path
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.YETI
    #dbc.themes.DARKLY
    #'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def load_data():
    #temp_file = Path('../resources/get_temp.out')
    temp_file = Path('/home/pi/get_temp.out')
    return pd.read_csv(temp_file, sep=' ', header=None, names=['date', 'time', 'temp'], parse_dates=[['date', 'time']])

def build_figure(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(df.date_time), y=list(df.temp)))
    fig.update_layout(
        #title_text="Gemessene Temperatur - DS18B20@dragonfly",
        xaxis_title="Datum",
        yaxis_title="Temperatur / °C",
        template='none'
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

df = load_data()

NAVBAR = dbc.NavbarSimple(
    brand="Raspberry Pi Temperaturmessung",
    brand_href="#",
    color="primary",
    dark=True,
)

def get_temp_graph(df):
    return dbc.Card(
        [
            dbc.CardHeader("Gemessene Temperatur im Zimmer 2 (Büro) - DS18B20@dragonfly"),
            dbc.CardBody(
                [
                    dcc.Graph(
                        id='example-graph',
                        figure=build_figure(df),
                        config={'displayModeBar': False}
                    )
                ]
            )
        ]
    )

def get_body(df):
    return dbc.Container(
        [
            get_temp_graph(df),
        ],
        className="mt-2 mb-3",
    )

def serve_layout():
    return html.Div(children=[
        NAVBAR,
        get_body(load_data())
    ])


app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
