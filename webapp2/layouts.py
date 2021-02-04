import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from figures import build_figure
from dataloader import DataProviderSingleton

cards = html.Div([
    dbc.CardDeck([
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Aktuelle Temperatur", className="card-title"),
                    html.H1("-- °C"),
                    html.P(
                        "Messwert vom 31.01.2021 14:04",
                        className="card-text",
                    )
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Temperaturdurchschnitt", className="card-title"),
                    html.H1("-- °C"),
                    html.P(
                        "Zeitraum: 11:04 - 14:04",
                        className="card-text",
                    )
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Veränderung", className="card-title"),
                    html.H1("--"),
                    html.P(
                        "Die aktuelle Veränderung kann steigend, sinkend oder stabil sein",
                        className="card-text",
                    )
                ]
            )
        )
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
                        figure=build_figure(DataProviderSingleton.getInstance().get_df()),
                        config={'displayModeBar': False}
                    ),
#                    dcc.RangeSlider(
#                        id='my-range-slider',
#                        min=0,
#                        max=20,
#                        step=0.5,
#                        value=[5, 15],
#                        className='ml-5 mr-5'
#                    )
                ]
            )
        )
    ], className="mt-sm-3 ml-sm-1 mr-sm-1"
    )])
    