import dash
from dash.dependencies import Output, Input, State
from dataloader import DataProviderSingleton
from figures import build_figure

# -- MOVE TO UTIL ?
import pandas as pd

def npdt2dtdt(npdt):
    return pd.Timestamp(npdt).to_pydatetime()
# -- end of MOVE TO UTIL

def update_xaxes(n):
    df = DataProviderSingleton.getInstance().get_df()
    n = min(len(df), n)
    df_small = df[df.date_time >= df.date_time.values[-n]]
    if len(df_small) >= 600:
        nth = int(len(df_small) / 300)
        df_small = df_small.iloc[::nth, :]
    fig = build_figure(df_small)
    #fig.update_layout(
    #    xaxis_range = [npdt2dtdt(df.date_time.values[-n]), npdt2dtdt(df.date_time.values[-1])]
    #)
    return fig

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
        df = DataProviderSingleton.getInstance().get_df()
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if '1h-button' in changed_id:
            return update_xaxes(60)
        elif '3h-button' in changed_id:
            return update_xaxes(3 * 60)
        elif '6h-button' in changed_id:
            return update_xaxes(6 * 60)
        elif '12h-button' in changed_id:
            return update_xaxes(12 * 60)
        elif '1d-button' in changed_id:
            return update_xaxes(24 * 60)
        elif '7d-button' in changed_id:
            return update_xaxes(7 * 24 * 60)
        elif '30d-button' in changed_id:
            return update_xaxes(30 * 24 * 60)
        elif '1y-button' in changed_id:
            return update_xaxes(365 * 24 * 60)
        elif 'all-button' in changed_id:
            return update_xaxes(len(df))
        # FIXME - replace build_figure by update_axes
        return build_figure(df)
