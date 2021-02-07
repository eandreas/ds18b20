import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dataloader import DataProviderSingleton
import pandas as pd

def get_cards():
    return html.Div([
    dbc.CardDeck([
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Aktuelle Temperatur", className="card-title"),
                    html.H1("--", id = 'current-temp-text',
                        style={
                            'color': 'skyblue'
                        }
                    ),
                    html.P(
                        [
                            "Messwert vom:",
                            html.Br(),
                            DataProviderSingleton.getInstance().get_latest_datetime().strftime('%d.%m.%Y, %H:%M Uhr')
                        ],
                        id = 'current-temp-datetime',
                        className="card-text"
                    )
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Temperaturdurchschnitt", className="card-title"),
                    html.H1("--", id = 'average-temp-text',
                        style={
                            'color': 'skyblue'
                        }
                    ),
                    html.P(
                        [
                            "Berücksichtigter Zeitraum:",
                            html.Br(),
                            "--",
                        ],
                        id = 'average-temp-datetime',
                        className="card-text"
                    )
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Veränderung", className="card-title"),
                    html.H1("--", id = 'temp-tendency-text',
                        style={
                            'color': 'skyblue'
                        }
                    ),
                    html.P(
                        "Die aktuelle Veränderung kann steigend, sinkend oder stabil sein",
                        className="card-text",
                    )
                ]
            )
        ),
    ], className="mt-3 ml-1 mr-1"
)])

def get_temp_graph():
    return html.Div([
    dbc.CardDeck([
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2("Temperaturverlauf", className="card-title"),
                    html.Div(
                        [
                            dbc.Button("1 h", id = '1h-button',outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("3 h", id = '3h-button', outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("6 h", id = '6h-button',outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("12 h", id = '12h-button',outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("1 d", id = '1d-button',outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("7 d", id = '7d-button',outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("30 d", id = '30d-button',outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("1 y", id = '1y-button',outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("all", id = 'all-button',outline = True, color = 'dark', size="sm", className="mr-1")
                        ], className = "mt-5"
                    ),
                    dcc.Graph(
                        id='live_temp_graph',
                        figure=DataProviderSingleton.getInstance().get_fig('fig_3h'),
                        config={'displayModeBar': False}
                    ),
                ]
            )
        )
    ], className="mt-sm-3 ml-sm-1 mr-sm-1"
    )])

def serve_layout():
    DataProviderSingleton.getInstance().clear_figures()
    DataProviderSingleton.getInstance().load_data()
    return html.Div(children=[
        get_cards(),
        get_temp_graph(),
        dcc.Interval(
            id='interval-component',
            interval = 60 * 1000, # in milliseconds
            n_intervals = 0
        )
    ])
    