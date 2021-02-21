import dash
import dash_bootstrap_components as dbc
from layouts import serve_layout

external_stylesheets = [dbc.themes.YETI]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
)

# adding meta-tag within header to enable responsive design on ios devices
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
