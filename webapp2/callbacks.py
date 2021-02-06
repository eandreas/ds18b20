import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_html_components as html
from dataloader import DataProviderSingleton

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
        if '1h-button' in changed_id and btn_1h is not None:
            return DataProviderSingleton.getInstance().get_fig_1h()
        elif '3h-button' in changed_id and btn_3h is not None:
            return DataProviderSingleton.getInstance().get_fig_3h()
        elif '6h-button' in changed_id and btn_6h is not None:
            return DataProviderSingleton.getInstance().get_fig_6h()
        elif '12h-button' in changed_id and btn_12h is not None:
            return DataProviderSingleton.getInstance().get_fig_12h()
        elif '1d-button' in changed_id and btn_1d is not None:
            return DataProviderSingleton.getInstance().get_fig_1d()
        elif '7d-button' in changed_id  and btn_7d is not None:
            return DataProviderSingleton.getInstance().get_fig_7d()
        elif '30d-button' in changed_id and btn_30d is not None:
            return DataProviderSingleton.getInstance().get_fig_30d()
        elif '1y-button' in changed_id and btn_1y is not None:
            return DataProviderSingleton.getInstance().get_fig_1y()
        elif 'all-button' in changed_id and btn_all is not None:
            return DataProviderSingleton.getInstance().get_fig_all()
        raise PreventUpdate

    @app.callback(
        Output('current-temp-text', 'children'),
        Output('current-temp-datetime', 'children'),
        Output('live_temp_graph', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_metrics(n):
        dps = DataProviderSingleton.getInstance()
        dps.load_data()
        ctt = f'{dps.get_current_C()} °C'
        ctd = [
            "Messwert vom:",
            html.Br(),
            dps.get_latest_datetime().strftime('%d.%m.%Y, %H:%M Uhr')
        ]
        dps.clear_figures()
        fig = dps.get_fig_1d()
        return ctt, ctd, fig

