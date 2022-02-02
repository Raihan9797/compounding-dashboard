import pandas as pd
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


app = dash.Dash(
    __name__
    , external_stylesheets=[dbc.themes.BOOTSTRAP]
    , meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)
server = app.server

### create components
principal_label = html.Label('Principal: ')
rate_label = html.Label('Rate: ')
time_label = html.Label('Time: ')
con_label = html.Label('Contribution: ')
type_con_label = html.Label('Frequency of Contribution: ')
stop_con_label = html.Label('Stop Contribution at month: ')
n_label = html.Label('Frequency of Compounding: ')

principal_input = dcc.Input(
    id = 'principal_input',
    type = 'number',
    value = 0.01,
)
rate_input = dcc.Input(
    id = 'rate_input',
    type = 'number',
    value = 1.00,
)
time_input = dcc.Input(
    id = 'time_input',
    type = 'number',
    value = 30,
)

con_input = dcc.Input(
    id = 'con_input',
    type = 'number',
    value = 0,
)
type_con_input = dcc.Input(
    id = 'type_con_input',
    type = 'number',
    value = 1,
)
stop_con_input = dcc.Input(
    id = 'stop_con_input',
    type = 'number',
    value = 36,
)
n_input = dcc.Input(
    id = 'n_input',
    type = 'number',
    value = 1,
)

def create_label_input_col(x_label, x_input):
    col = dbc.Col(
        [
            x_label,
            x_input,
        ],
        width = 6,
        lg = {
            'size' : 3,
        },
        # md = {
        #     'size' : 6,
        # },
        # sm = {
        #     'size' : 6,
        # },
        xs = {
            'size' : 12,
        },
        style = {
            'border' : 'solid green',
            'display':'flex',
            'flex-direction':'column',
            'align-items': 'center',
        }
    )

    return col

row_col_input = dbc.Row(
    [
        create_label_input_col(principal_label, principal_input),
        create_label_input_col(rate_label, rate_input),
        create_label_input_col(time_label, time_input),
        create_label_input_col(con_label, con_input),
        create_label_input_col(type_con_label, type_con_input),
    ]
)

lg_input = dbc.ListGroup(
    [
        dbc.ListGroupItem(
            [
                principal_label,
                principal_input,
            ],
        ),
        dbc.ListGroupItem(
            [
                rate_label,
                rate_input,
            ],
        ),
        dbc.ListGroupItem(
            [
                time_label,
                time_input,
            ],
        ),
        dbc.ListGroupItem(
            [
                con_label,
                con_input,
            ],
        ),
        # dbc.ListGroupItem(
        #     [
        #         html.Div(
        #             [
        #                 con_label,
        #                 con_input,
        #             ],
        #             style = {
        #                 'display': 'flex',
        #                 'flex-direction': 'column',
        #                 'border': 'solid green',
        #             }
        #         ),
        #     ]
        # ),

    ],
    className = 'lg-6 mb-md-6 mb-sm-12 mb-xs-12 d-flex align-items-center',
    horizontal=True,
)

layout = dbc.Container(
    [
        # row_col_input
        lg_input,
    ],
    # fluid = True,
)
app.layout = layout

if __name__ == '__main__':
    app.run_server(
        debug = True
        , use_reloader = True
        , port = 4000
    )