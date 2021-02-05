import dash
from dash.dependencies import Output, Input, State
from dataloader import DataProviderSingleton

# -- MOVE TO UTIL ?
import pandas as pd

def npdt2dtdt(npdt):
    return pd.Timestamp(npdt).to_pydatetime()
# -- end of MOVE TO UTIL

def register_callbacks(app):
    
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
            return DataProviderSingleton.getInstance().get_fig_1h()
        elif '3h-button' in changed_id:
            return DataProviderSingleton.getInstance().get_fig_3h()
        elif '6h-button' in changed_id:
            return DataProviderSingleton.getInstance().get_fig_6h()
        elif '12h-button' in changed_id:
            return DataProviderSingleton.getInstance().get_fig_12h()
        elif '1d-button' in changed_id:
            return DataProviderSingleton.getInstance().get_fig_1d()
        elif '7d-button' in changed_id:
            return DataProviderSingleton.getInstance().get_fig_7d()
        elif '30d-button' in changed_id:
            return DataProviderSingleton.getInstance().get_fig_30d()
        elif '1y-button' in changed_id:
            return DataProviderSingleton.getInstance().get_fig_1y()
        elif 'all-button' in changed_id:
            return DataProviderSingleton.getInstance().get_fig_all()
        return DataProviderSingleton.getInstance().get_fig_all()
