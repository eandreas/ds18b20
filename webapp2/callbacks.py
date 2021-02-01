import dash
from dash.dependencies import Output, Input, State
from dataloader import load_data
from figures import build_figure

# -- MOVE TO UTIL ?
import pandas as pd

def npdt2dtdt(npdt):
    return pd.Timestamp(npdt).to_pydatetime()
# -- end of MOVE TO UTIL

def update_xaxes(df, fig, n):
    n = min(len(df), n)
    fig.update_layout(
        xaxis_range = [npdt2dtdt(df.date_time.values[-n]), npdt2dtdt(df.date_time.values[-1])]
    )
    return fig

def register_callbacks(app, df, fig):
    
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
            return update_xaxes(df, fig, 60)
        elif '3h-button' in changed_id:
            return update_xaxes(df, fig, 3 * 60)
        elif '6h-button' in changed_id:
            return update_xaxes(df, fig, 6 * 60)
        elif '12h-button' in changed_id:
            return update_xaxes(df, fig, 12 * 60)
        elif '1d-button' in changed_id:
            return update_xaxes(df, fig, 24 * 60)
        elif '7d-button' in changed_id:
            return update_xaxes(df, fig, 7 * 24 * 60)
        elif '30d-button' in changed_id:
            return update_xaxes(df, fig, 30 * 24 * 60)
        elif '1y-button' in changed_id:
            return update_xaxes(df, fig, 365 * 24 * 60)
        # FIXME - replace build_figure by update_axes
        return build_figure(df)