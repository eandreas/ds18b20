import dash
from dash.dependencies import Output, Input, State
from dataloader import load_data
from figures import build_figure

# -- MOVE TO UTIL ?
import pandas as pd

def npdt2dtdt(npdt):
    return pd.Timestamp(npdt).to_pydatetime()
# -- end of MOVE TO UTIL

def update_xaxes(df, n):
    n = min(len(df), n)
    print(f'df starts at {df.date_time.values[0]} and ends at {df.date_time.values[-1]}')
    print(f'Filtering df for datetimes>={df.date_time.values[-n]}')
    df_small = df[df.date_time >= df.date_time.values[-n]]
    print(f'df_small starts at {df_small.date_time.values[0]} and ends at {df_small.date_time.values[-1]}')
    if len(df_small) >= 600:
        nth = int(len(df_small) / 300)
        df_small = df_small.iloc[::nth, :]
    fig = build_figure(df_small)
    #fig.update_layout(
    #    xaxis_range = [npdt2dtdt(df.date_time.values[-n]), npdt2dtdt(df.date_time.values[-1])]
    #)
    return fig

def register_callbacks(app, df):
    
    @app.callback(
        Output('live_temp_graph', 'figure'),
        [
            Input('1h-button', 'n_clicks'),
            Input('3h-button', 'n_clicks'),
            Input('6h-button', 'n_clicks'),
            Input('12h-button', 'n_clicks'),
            Input('1d-button', 'n_clicks'),
            Input('7d-button', 'n_clicks'),
            Input('30d-button', 'n_clicks'),
            Input('1y-button', 'n_clicks'),
            Input('all-button', 'n_clicks')
        ]
    )
    def update_output(btn_1h, btn_3h, btn_6h, btn_12h, btn_1d, btn_7d, btn_30d, btn_1y, btn_all):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if '1h-button' in changed_id:
            return update_xaxes(df, 60)
        elif '3h-button' in changed_id:
            return update_xaxes(df, 3 * 60)
        elif '6h-button' in changed_id:
            return update_xaxes(df, 6 * 60)
        elif '12h-button' in changed_id:
            return update_xaxes(df, 12 * 60)
        elif '1d-button' in changed_id:
            return update_xaxes(df, 24 * 60)
        elif '7d-button' in changed_id:
            return update_xaxes(df, 7 * 24 * 60)
        elif '30d-button' in changed_id:
            return update_xaxes(df, 30 * 24 * 60)
        elif '1y-button' in changed_id:
            return update_xaxes(df, 365 * 24 * 60)
        elif 'all-button' in changed_id:
            return update_xaxes(df, len(df))
        # FIXME - replace build_figure by update_axes
        return build_figure(df)