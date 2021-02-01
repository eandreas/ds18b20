import dash
from dash.dependencies import Output, Input, State
from dataloader import load_data
from figures import build_figure

def register_callbacks(app, df):
    
    @app.callback(
        Output('live_temp_graph', 'figure'),
        Input('1h-button', 'n_clicks'),
        Input('3h-button', 'n_clicks'),
        Input('6h-button', 'n_clicks'),
        Input('12h-button', 'n_clicks'),
        Input('1d-button', 'n_clicks'),
        Input('7d-button', 'n_clicks'),
        Input('30d-button', 'n_clicks'),
        Input('1y-button', 'n_clicks'),
        Input('all-button', 'n_clicks')
    )
    def update_output(btn_1h, btn_3h, btn_6h, btn_12h, btn_1d, btn_7d, btn_30d, btn_1y, btn_all):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if '1h-button' in changed_id:
            return build_figure(df, 60)
        elif '3h-button' in changed_id:
            return build_figure(df, 3 * 60)
        elif '6h-button' in changed_id:
            return build_figure(df, 6 * 60)
        elif '12h-button' in changed_id:
            return build_figure(df, 12 * 60)
        elif '1d-button' in changed_id:
            return build_figure(df, 24 * 60)
        elif '7d-button' in changed_id:
            return build_figure(df, 7 * 24 * 60)
        elif '30d-button' in changed_id:
            return build_figure(df, 30 * 24 * 60)
        elif '1y-button' in changed_id:
            return build_figure(df, 365 * 24 * 60)
        return build_figure(df)