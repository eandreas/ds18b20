import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts import cards, get_temp_graph
from figures import build_figure
from dataloader import load_data
from callbacks import register_callbacks

external_stylesheets = [dbc.themes.YETI]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def serve_layout():
    df = load_data(caller='serve_layout')
    register_callbacks(app, df)
    return html.Div(children=[
        cards,
        get_temp_graph(df)
    ])

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)