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
        Input('all-button', 'n_clicks'),
        Input('interval-component', 'n_intervals')
    )
    def update_figure(btn_1h, btn_3h, btn_6h, btn_12h, btn_1d, btn_7d, btn_30d, btn_1y, btn_all, n):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        #print(f'triggered={input_id}')
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        if input_id == 'interval-component':
            dps = DataProviderSingleton.getInstance()
            dps.load_data()
            dps.clear_figures()
            return dps.get_fig_7d()
        elif input_id == '1h-button':
            return DataProviderSingleton.getInstance().get_fig_1h()
        elif input_id == '3h-button':
            return DataProviderSingleton.getInstance().get_fig_3h()
        elif input_id == '6h-button':
            return DataProviderSingleton.getInstance().get_fig_6h()
        elif input_id == '12h-button':
            return DataProviderSingleton.getInstance().get_fig_12h()
        elif input_id == '1d-button':
            return DataProviderSingleton.getInstance().get_fig_1d()
        elif input_id == '7d-button':
            return DataProviderSingleton.getInstance().get_fig_7d()
        elif input_id == '30d-button':
            return DataProviderSingleton.getInstance().get_fig_30d()
        elif input_id == '1y-button':
            return DataProviderSingleton.getInstance().get_fig_1y()
        elif input_id == 'all-button':
            return DataProviderSingleton.getInstance().get_fig_all()
        raise PreventUpdate

    @app.callback(
        Output('current-temp-text', 'children'),
        Output('current-temp-datetime', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_cards(n):
        dps = DataProviderSingleton.getInstance()
        dps.load_data()
        ctt = f'{dps.get_current_C()} °C'
        ctd = [
            "Messwert vom:",
            html.Br(),
            dps.get_latest_datetime().strftime('%d.%m.%Y, %H:%M Uhr')
        ]
        return ctt, ctd

