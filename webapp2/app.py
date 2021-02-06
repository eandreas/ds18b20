import dash
import dash_bootstrap_components as dbc
from callbacks import register_callbacks
from layouts import serve_layout

external_stylesheets = [dbc.themes.YETI]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
register_callbacks(app)

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8081)