import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

### create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


### import and clean data
def compound_interest(principal, rate, time, dca = 0, n = 1):
    amount = principal * (1 + rate/(100 * n)) ** (time * n)
    principal += dca
    return amount

def compound_interestv2(p, r, t, pmt = 0, n = 12):
    """
    p: principal
    r: interest rate in decimal (3.75% -> 0.0375)
    t: time in years (do 1/12 for 1 month)
    pmt: monthly contribution
    n: number of times compounded per year (12 for monthly, 365 for daily)

    return: amount = cpd growth of principal + cpd growth of contributions
    """
    # form1
    main_val = p * (1 + r / n) ** (n * t)
    add_val = (pmt * (1 + r / n) ** (n * t) - pmt) / (r / n)
    print(main_val)
    print(add_val)

    amount = main_val + add_val
    return amount

def cpd_interest_v4(p, r, t, con, type_con, stop_con, n):
    """
    p: principal
    r: interest rate in decimal (3.75% -> 0.0375)
    t: time in years (do 1/12 for 1 month)
    con: contribution made
    type_con: int, how many times a contribution is made in a year (1 == monthly, 3 == quarterly)
    stop_con: months before stopping contributions
    n: number of times compounded per year (12 for monthly, 365 for daily)

    return: amount = cpd growth of principal + cpd growth of contributions
    """
    # try and start simple first: basic compounding
    months = []
    principals = [p for i in range(1, t*n + 1)]

    amount = p
    amounts = []

    interest_earned = 0
    interests = []
    cum_interest_earned = 0
    cum_interests = []

    total_contributions = 0
    contributions = []
    cum_contributions = []
    for i in range(1, t * n + 1):
        months.append(i)

        # check when to contribute
        if i % type_con != 0 or i >= stop_con:
            amount += 0
            total_contributions += 0
            contributions.append(0)
            cum_contributions.append(total_contributions)
        else:
            # print('adding con')
            amount += con
            total_contributions += con
            contributions.append(con)
            cum_contributions.append(total_contributions)


        old_amount = amount
        amount = amount * (1 + r/n)
        interest_earned = (amount - old_amount)
        interests.append(interest_earned)
        cum_interest_earned += amount - old_amount

        cum_interests.append(cum_interest_earned)
        # print(amount)
        amounts.append(amount)

    print("Final Amount: ", amount)
    print("Total interest earned: ", cum_interest_earned)
    print("Total contributions: ", total_contributions)

    df = pd.DataFrame(list(zip(months, principals, amounts, interests, cum_interests, contributions, cum_contributions)), columns = ['Month', 'Principal', 'Amount', 'Interest', 'Cumulative_Interest', 'Contribution', 'Cumulative_Contribution'])
    return df

def create_cpd_fig_v2(df):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(name = 'Principal', x = df.Month, y = df.Principal)
    )
    fig.add_trace(
        go.Bar(name = 'Contribution', x = df.Month, y = df.Cumulative_Contribution)
    )
    fig.add_trace(
        go.Bar(name = 'Interest', x = df.Month, y = df.Cumulative_Interest)
    )

    fig.update_layout(barmode = 'stack')
    return fig

def create_cpd_df(principal, rate, timespan, dca = 0, n = 1):
    rows = []

    for t in range(0, timespan + 1):
        amount = compound_interest(principal, rate, t)

        interest = amount - principal
        # print(interest)
        # print(amount)
        rows.append([t, principal,interest, amount])
    
    df = pd.DataFrame(data = rows, columns=['year', 'principal', 'interest', 'amount'], )
    df = df.round(2)
    return df

def create_cpd_fig(df1):
    customdata_df = df1
    hovertemplate = """
        Total Amount: %{customdata[3]}<br>
        Interest: %{customdata[2]} <br>
        Principal: %{customdata[1]} <extra></extra>
        """
        # "Interest: %{customdata[2]} <br>" +\
        # "Principal: %{customdata[1]} <br>" +\
        # "Total Amount : " + "%{customdata[3]}<extra></extra>"
    print(hovertemplate)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name = 'principal',
        x = df1.year, y = df1.principal,
        customdata = customdata_df,
        hovertemplate = hovertemplate,
    ))
    fig.add_trace(go.Bar(
        name = 'interest',
        x = df1.year, y = df1.interest,
        customdata = customdata_df,
        text = df1.amount,
        hovertemplate = hovertemplate,
    ))
    fig.update_layout(barmode = 'stack')

    fig.update_layout(
        title="Compounded return over time",
        xaxis_title="Time Periods",
        yaxis_title="Amount",
        legend_title="Legend Title",
        hovermode = 'x unified',
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )

    return fig

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
    value = 100,
)
rate_input = dcc.Input(
    id = 'rate_input',
    type = 'number',
    value = 10,
)
time_input = dcc.Input(
    id = 'time_input',
    type = 'number',
    value = 20,
)

principal_input2 = dcc.Input(
    id = 'principal_input2',
    type = 'number',
    value = 100,
)
rate_input2 = dcc.Input(
    id = 'rate_input2',
    type = 'number',
    value = 10,
)
time_input2 = dcc.Input(
    id = 'time_input2',
    type = 'number',
    value = 20,
)

con_input2 = dcc.Input(
    id = 'con_input2',
    type = 'number',
    value = 20,
)
type_con_input2 = dcc.Input(
    id = 'type_con_input2',
    type = 'number',
    value = 20,
)
stop_con_input2 = dcc.Input(
    id = 'stop_con_input2',
    type = 'number',
    value = 20,
)
n_input2 = dcc.Input(
    id = 'n_input2',
    type = 'number',
    value = 20,
)

### callbacks
@app.callback(
    [
        Output('cpd_bar', 'figure'),
        Output('test_div', 'children'),
    ],
    [
        Input('principal_input', 'value'),
        Input(component_id='rate_input', component_property='value'),
        Input('time_input', 'value'),
    ],
    # prevent_initial_callback = True,
)
def update_cpd_bar(principal, rate, time):
    # if null vals, dont update the graph
    if rate == None or principal == None or time == None:
        raise dash.exceptions.PreventUpdate
    else:
        df1 = create_cpd_df(principal, rate, time)
        print('UPDATE 1')
        print(df1)
        fig1 = create_cpd_fig(df1)


        return fig1, rate

@app.callback(
    [
        Output('cpd_bar2', 'figure'),
    ],
    [
        Input('principal_input2', 'value'),
        Input(component_id='rate_input2', component_property='value'),
        Input('time_input2', 'value'),
    ],
    # prevent_initial_callback = True,
)
def update_cpd_bar2(principal2, rate2, time2):
    # if null vals, dont update the graph
    if rate2 == None or principal2 == None or time2 == None:
        raise dash.exceptions.PreventUpdate
    else:
        df1 = create_cpd_df(principal2, rate2, time2)
        print('UPDATE 2')
        print(df1)
        fig1 = create_cpd_fig(df1)


        return [fig1]

### app layout and bigger components
bar_card = dbc.Card(
    [
        dbc.CardHeader("Testing header"),
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'cpd_bar',
                                    figure = {}
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        principal_label,
                                        principal_input,
                                    ]
                                ),
                                html.Div(
                                    [
                                        rate_label,
                                        rate_input,

                                    ]
                                ),
                                html.Div(
                                    [
                                        time_label,
                                        time_input,

                                    ]
                                ),
                            ],
                            style = {
                                'border': 'solid pink',
                                'display': 'flex',
                                'justify-content': 'space-around',
                            },
                        ),
                    ],
                    style = {
                        'display' : 'flex',
                        'flex-direction': 'column',
                    },
                ),
            ]
        )
    ]
)
bar_card2 = dbc.Card(
    [
        dbc.CardHeader("Testing header"),
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'cpd_bar2',
                                    figure = {}
                                ),
                            ]
                        ),
                        html.Br(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        principal_label,
                                        principal_input2,
                                    ]
                                ),
                                html.Div(
                                    [
                                        rate_label,
                                        rate_input2,

                                    ]
                                ),
                                html.Div(
                                    [
                                        time_label,
                                        time_input2,

                                    ]
                                ),
                                # new addition
                                html.Div(
                                    [
                                        con_label,
                                        con_input2,
                                    ]
                                ),
                                html.Div(
                                    [
                                        type_con_label,
                                        type_con_input2,
                                    ]
                                ),
                                html.Div(
                                    [
                                        stop_con_label,
                                        stop_con_input2,
                                    ]
                                ),
                                html.Div(
                                    [
                                        n_label,
                                        n_input2,
                                    ]
                                ),
                            ],
                            style = {
                                'border': 'solid pink',
                                'display': 'flex',
                                'justify-content': 'space-around',
                            },
                        ),
                    ],
                    style = {
                        'display' : 'flex',
                        'flex-direction': 'column',
                    },
                ),
                # dbc.Container(
                #     [
                #         dbc.Row(
                #             [
                #                 dcc.Graph(
                #                     id = 'cpd_bar2',
                #                     figure = {}
                #                 ),
                #             ]
                #         ),
                #         # dbc.Row(
                #         #     [
                #         #         dbc.Col(
                #         #             [
                #         #                 html.Label('Principal: '),
                #         #                 #principal_input2,
                #         #             ],
                #         #             align = 'center',
                #         #             width = {
                #         #                 'size': 2.5,
                #         #             },
                #         #             style = {
                #         #                 'display': 'flex',
                #         #                 'border': 'solid blue',
                #         #             },
                #         #         ),
                #         #         dbc.Col(
                #         #             [
                #         #                 html.Label('Rate: '),
                #         #                 #rate_input2,
                #         #             ],
                #         #             align = 'center',
                #         #             width = {
                #         #                 'size': 2.5,
                #         #             },
                #         #             style = {
                #         #                 'border': 'solid blue',
                #         #             }
                #         #         ),
                #         #         dbc.Col(
                #         #             [
                #         #                 html.Label('Time Period: '),
                #         #                 #time_input2,
                #         #             ],
                #         #             align = 'center',
                #         #             width = {
                #         #                 'size': 2.5,
                #         #             },
                #         #             style = {
                #         #                 'border': 'solid blue',
                #         #             }
                #         #         ),
                #         #     ],
                #         #     justify= 'center'
                #         # )

                #     ],
                #     fluid=True,
                #     style= {
                #         'border': 'solid yellow',
                #     },
                # ),
            ]
        )
    ]
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            'The Compound Effect Visualized',
                            style= {
                                'textAlign': 'center',
                            }
                        ),
                    ],
                    style = {
                        'border': 'solid blue',
                    }
                ),
            ],
            style = {
                'border': 'solid green',
            },
        ),

        # dbc.Row(
        #     [
        #         dbc.Col(
        #             [
        #                 html.Label('Principal: '),
        #                 principal_input,
        #             ],
        #             align = 'center',
        #             width = {
        #                 'size': 2.5,
        #             },
        #             style = {
        #                 'display': 'flex',
        #                 'border': 'solid blue',
        #             },
        #         ),
        #         dbc.Col(
        #             [
        #                 html.Label('Rate: '),
        #                 rate_input,
        #             ],
        #             align = 'center',
        #             width = {
        #                 'size': 2.5,
        #             },
        #             style = {
        #                 'border': 'solid blue',
        #             }
        #         ),
        #         dbc.Col(
        #             [
        #                 html.Label('Time Period: '),
        #                 time_input,
        #             ],
        #             align = 'center',
        #             width = {
        #                 'size': 2.5,
        #             },
        #             style = {
        #                 'border': 'solid blue',
        #             }
        #         ),
        #     ],
        #     justify = 'start',
        # ),


        html.Div(id = 'test_div'),

        # dcc.Graph(
        #     id = 'cpd_bar',
        #     figure = {}
        # ),
        bar_card,



        bar_card2,


    ],
    style = {
        'border': 'solid red',
    },
    fluid = True,
)

app.layout = layout


if __name__ == '__main__':
    app.run_server(debug = True)