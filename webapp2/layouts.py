import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dataloader import load_data
from figures import build_figure

cards = html.Div([
    dbc.CardDeck([
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Aktuelle Temperatur", className="card-title"),
                    html.H1("21.3 °C"),
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
                    html.H1("23.8 °C"),
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
                    html.H1("sinkend"),
                    html.P(
                        "Die aktuelle Veränderung kann steigend, sinkend oder stabil sein",
                        className="card-text",
                    )
                ]
            )
        )
    ], className="mt-3 ml-1 mr-1"
)])

temp_graph = html.Div([
    dbc.CardDeck([
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2("Temperaturverlauf", className="card-title"),
                    html.Div(
                        [
                            dbc.Button("1 h", outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("3 h", id = '3h-button', outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("6 h", outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("12 h", outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("1 d", outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("7 d", outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("1 m", outline = True, color = 'dark', size="sm", className="mr-1"),
                            dbc.Button("1 y", outline = True, color = 'dark', size="sm", className="mr-1")
                        ], className = "mt-5"
                    ),
                    dcc.Graph(
                        id='live_temp_graph',
                        figure=build_figure(load_data()),
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

def serve_layout():
    return html.Div(children=[
        cards,
        temp_graph
    ])