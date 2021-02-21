import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output, State
# from dataloader import DataProviderSingleton
# import pandas as pd
from figures import serve_figure

card_content_1 = [
    # dbc.CardHeader("Aktuelle Temperatur"),
    dbc.CardBody(
        children=[
            html.H2("21.4 °C", className="card-title"),
            html.P(
                [
                    "Messwert vom:",
                    html.Br(),
                    "20. Februar 21:56 Uhr",
                ],
                className="card-text",
            )
        ]
    ),
]

card_content_2 = [
    # dbc.CardHeader("Durchschnittstemperatur"),
    dbc.CardBody(
        [
            html.H2("20.1 °C", className="card-title"),
            html.P(
                [
                    "Berücksichtigter Zeitraum:",
                    html.Br(),
                    "--"
                ],
                className="card-text",
            ),
        ]
    ),
]

card_content_3 = [
    # dbc.CardHeader("Veränderung"),
    dbc.CardBody(
        [
            html.H2("stabil", className="card-title"),
            html.P(
                "Die Aktuelle veränderung kann steigend, sinkend oder stabil sein.",
                className="card-text",
            ),
        ]
    ),
]

navbar = dbc.NavbarSimple(
    children=[],
    brand="Temperature Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)


def serve_layout():
    return html.Div([
        navbar,
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(card_content_1, color="light", outline=True),
                                className="col-md-4 col-12 mt-3"),
                        dbc.Col(dbc.Card(card_content_2, color="light", outline=True),
                                className="col-md-4 col-12 mt-3"),
                        dbc.Col(dbc.Card(card_content_3, color="light", outline=True),
                                className="col-md-4 col-12 mt-3"),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(card_content_1, color="light", outline=True),
                                className="col-12 mt-3 mb-3"),
                    ],
                )
            ],
            fluid=True
        )])
