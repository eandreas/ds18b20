import dash
import dash_bootstrap_components as dbc
from layouts import serve_layout
from callbacks import register_callbacks

external_stylesheets = [dbc.themes.YETI]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = serve_layout

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)