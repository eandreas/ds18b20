import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts import cards, get_temp_graph
from figures import build_figure
from dataloader import DataProviderSingleton, load_data
from callbacks import register_callbacks

external_stylesheets = [dbc.themes.YETI]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
register_callbacks(app)

def serve_layout():
    DataProviderSingleton.getInstance().set_df(load_data())
    return html.Div(children=[
        cards,
        get_temp_graph()
    ])

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)