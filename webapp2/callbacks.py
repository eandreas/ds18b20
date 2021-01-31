from dash.dependencies import Output, Input, State
from dataloader import load_data
from figures import build_figure

def register_callbacks(app):
    
    @app.callback(
        Output('live_temp_graph', 'figure'),
        Input('3h-button', 'n_clicks')
    )
    def update_output(n_clicks):
        df = load_data()
        if n_clicks is None:
            return build_figure(df)
        else:
            return build_figure(df, 180)