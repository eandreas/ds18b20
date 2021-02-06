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
            return dps.get_fig(DataProviderSingleton.getInstance().get_last_fig_id())
        elif input_id == '1h-button':
            fig_id = 'fig_1h'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
        elif input_id == '3h-button':
            fig_id = 'fig_3h'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
        elif input_id == '6h-button':
            fig_id = 'fig_6h'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
        elif input_id == '12h-button':
            fig_id = 'fig_12h'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
        elif input_id == '1d-button':
            fig_id = 'fig_1d'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
        elif input_id == '7d-button':
            fig_id = 'fig_7d'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
        elif input_id == '30d-button':
            fig_id = 'fig_30d'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
        elif input_id == '1y-button':
            fig_id = 'fig_1y'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
        elif input_id == 'all-button':
            fig_id = 'fig_all'
            DataProviderSingleton.getInstance().set_last_fig_id(fig_id)
            return DataProviderSingleton.getInstance().get_fig(fig_id)
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

