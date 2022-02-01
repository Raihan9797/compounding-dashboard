import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

### create app
app = dash.Dash(
    __name__
    , external_stylesheets=[dbc.themes.SLATE]
    , meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)
server = app.server


### import and clean data
# def compound_interest(principal, rate, time, dca = 0, n = 1):
#     amount = principal * (1 + rate/(100 * n)) ** (time * n)
#     principal += dca
#     return amount
# 
# def compound_interestv2(p, r, t, pmt = 0, n = 12):
#     """
#     p: principal
#     r: interest rate in decimal (3.75% -> 0.0375)
#     t: time in years (do 1/12 for 1 month)
#     pmt: monthly contribution
#     n: number of times compounded per year (12 for monthly, 365 for daily)
# 
#     return: amount = cpd growth of principal + cpd growth of contributions
#     """
#     # form1
#     main_val = p * (1 + r / n) ** (n * t)
#     add_val = (pmt * (1 + r / n) ** (n * t) - pmt) / (r / n)
#     print(main_val)
#     print(add_val)
# 
#     amount = main_val + add_val
#     return amount

def cpd_interest_v4_2(p, r, t, con, type_con, start_con, stop_con, n):
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
        if i % type_con != 0 or i < start_con or i > stop_con:
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
    df = df.round(2)
    return df
# def cpd_interest_v4(p, r, t, con, type_con, stop_con, n):
#     """
#     p: principal
#     r: interest rate in decimal (3.75% -> 0.0375)
#     t: time in years (do 1/12 for 1 month)
#     con: contribution made
#     type_con: int, how many times a contribution is made in a year (1 == monthly, 3 == quarterly)
#     stop_con: months before stopping contributions
#     n: number of times compounded per year (12 for monthly, 365 for daily)
# 
#     return: amount = cpd growth of principal + cpd growth of contributions
#     """
#     # try and start simple first: basic compounding
#     months = []
#     principals = [p for i in range(1, t*n + 1)]
# 
#     amount = p
#     amounts = []
# 
#     interest_earned = 0
#     interests = []
#     cum_interest_earned = 0
#     cum_interests = []
# 
#     total_contributions = 0
#     contributions = []
#     cum_contributions = []
#     for i in range(1, t * n + 1):
#         months.append(i)
# 
#         # check when to contribute
#         if i % type_con != 0 or i >= stop_con:
#             amount += 0
#             total_contributions += 0
#             contributions.append(0)
#             cum_contributions.append(total_contributions)
#         else:
#             # print('adding con')
#             amount += con
#             total_contributions += con
#             contributions.append(con)
#             cum_contributions.append(total_contributions)
# 
# 
#         old_amount = amount
#         amount = amount * (1 + r/n)
#         interest_earned = (amount - old_amount)
#         interests.append(interest_earned)
#         cum_interest_earned += amount - old_amount
# 
#         cum_interests.append(cum_interest_earned)
#         # print(amount)
#         amounts.append(amount)
# 
#     print("Final Amount: ", amount)
#     print("Total interest earned: ", cum_interest_earned)
#     print("Total contributions: ", total_contributions)
# 
#     df = pd.DataFrame(list(zip(months, principals, amounts, interests, cum_interests, contributions, cum_contributions)), columns = ['Month', 'Principal', 'Amount', 'Interest', 'Cumulative_Interest', 'Contribution', 'Cumulative_Contribution'])
#     df = df.round(2)
#     return df
# def create_cpd_fig_v3(df):
#     ### trying to use px, stacked value hovers are there but still weird.
#     fig = px.bar(
#         df, x="Month"
#         , y=["Principal", "Cumulative_Contribution", "Cumulative_Interest"]
#         , title="Wide-Form Input"
#         , hover_name = "Month"
#         , hover_data = ["Amount"]
#         )
#     return fig

def create_cpd_fig_v2(df):
    fig = go.Figure()
    ### trying to get a nice hover template which includes
    ### amt, principak, cuminterest, cumcontribution
    ### values available, but formatting is really bad.
    customdata_df = df[['Amount', 'Principal', 'Cumulative_Interest', 'Cumulative_Contribution']]
    hovertemplate = """
        %{customdata[1]} <br>
        Total Amount: %{customdata[0]}<br>
        """
        # Principal: %{customdata[1]} <br>
        # Interest: %{customdata[2]} <br>
        # Contribution: %{customdata[3]} <br>
    # print(hovertemplate)
    # print(customdata_df.columns)


    fig.add_trace(go.Bar(
        name = 'Principal',
        x = df.Month, y = df.Principal,
        # customdata = customdata_df,
        # hovertemplate = hovertemplate,
    ))
    # fig.add_trace(
    #     go.Bar(name = 'Principal', x = df.Month, y = df.Principal)
    # )
    fig.add_trace(go.Bar(
        name = 'Contribution'
        , x = df.Month, y = df.Cumulative_Contribution,
        # customdata = customdata_df,
        # hovertemplate = hovertemplate,
    ))
    fig.add_trace(
        go.Bar(
            name = 'Interest'
            , x = df.Month, y = df.Cumulative_Interest,
            textposition = 'auto', text = df.Amount,
        )
    )

    fig.update_layout(barmode = 'stack', template = 'plotly_dark')
    fig.update_traces(texttemplate='%{text:.3s}', textposition='outside')

    fig.update_layout(
        title="Compounded return over time",
        title_x = 0.5,
        xaxis_title="Time Periods",
        yaxis_title="Amount",
        # legend_title="Legend Title",
        hovermode = 'x unified',
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y= -0.5,
        xanchor="right",
        x=1
    ))
    return fig

# def create_cpd_df(principal, rate, timespan, dca = 0, n = 1):
#     rows = []
# 
#     for t in range(0, timespan + 1):
#         amount = compound_interest(principal, rate, t)
# 
#         interest = amount - principal
#         # print(interest)
#         # print(amount)
#         rows.append([t, principal,interest, amount])
#     
#     df = pd.DataFrame(data = rows, columns=['year', 'principal', 'interest', 'amount'], )
#     df = df.round(2)
#     return df

# def create_cpd_fig(df1):
#     customdata_df = df1
#     hovertemplate = """
#         Total Amount: %{customdata[3]}<br>
#         Interest: %{customdata[2]} <br>
#         Principal: %{customdata[1]} <extra></extra>
#         """
#         # "Interest: %{customdata[2]} <br>" +\
#         # "Principal: %{customdata[1]} <br>" +\
#         # "Total Amount : " + "%{customdata[3]}<extra></extra>"
#     print(hovertemplate)
# 
#     fig = go.Figure()
# 
#     fig.add_trace(go.Bar(
#         name = 'principal',
#         x = df1.year, y = df1.principal,
#         customdata = customdata_df,
#         hovertemplate = hovertemplate,
#     ))
#     fig.add_trace(go.Bar(
#         name = 'interest',
#         x = df1.year, y = df1.interest,
#         customdata = customdata_df,
#         text = df1.amount,
#         hovertemplate = hovertemplate,
#     ))
#     fig.update_layout(barmode = 'stack')
# 
#     fig.update_layout(
#         title="Compounded return over time",
#         xaxis_title="Time Periods",
#         yaxis_title="Amount",
#         legend_title="Legend Title",
#         hovermode = 'x unified',
#         # font=dict(
#         #     family="Courier New, monospace",
#         #     size=18,
#         #     color="RebeccaPurple"
#         # )
#     )
# 
#     return fig

### create components
principal_label = html.Label('Principal: ')
rate_label = html.Label('Rate: ')
time_label = html.Label('Time: ')
con_label = html.Label('Contribution: ')
type_con_label = html.Label('Frequency of Contribution: ')
start_con_label = html.Label('Start Contribution at period: ')
stop_con_label = html.Label('Stop Contribution at period: ')
n_label = html.Label('Frequency of Compounding: ')

principal_input = dcc.Input(
    id = 'principal_input',
    type = 'number',
    value = 0.00,
    max = 1_000_000,
    min = -1_000_000,
)
rate_input = dcc.Input(
    id = 'rate_input',
    type = 'number',
    value = 0.1,
)
time_input = dcc.Input(
    id = 'time_input',
    type = 'number',
    value = 65,
    step = 1,
)

con_input = dcc.Input(
    id = 'con_input',
    type = 'number',
    value = 2_000,
)
type_con_input = dcc.Input(
    id = 'type_con_input',
    type = 'number',
    value = 1,
    min = 1,
)
start_con_input = dcc.Input(
    id = 'start_con_input',
    type = 'number',
    value = 19,
)
stop_con_input = dcc.Input(
    id = 'stop_con_input',
    type = 'number',
    value = 25,
)
n_input = dcc.Input(
    id = 'n_input',
    type = 'number',
    value = 1,
)


### bar 2 inputs
principal_input2 = dcc.Input(
    id = 'principal_input2',
    type = 'number',
    value = 0,
    max = 1_000_000,
    min = -1_000_000,
)
rate_input2 = dcc.Input(
    id = 'rate_input2',
    type = 'number',
    value = 0.1,
)
time_input2 = dcc.Input(
    id = 'time_input2',
    type = 'number',
    value = 65,
    step = 1,
)

con_input2 = dcc.Input(
    id = 'con_input2',
    type = 'number',
    value = 2_000,
)
type_con_input2 = dcc.Input(
    id = 'type_con_input2',
    type = 'number',
    value = 1,
    min = 1,
)
start_con_input2 = dcc.Input(
    id = 'start_con_input2',
    type = 'number',
    value = 26,
)
stop_con_input2 = dcc.Input(
    id = 'stop_con_input2',
    type = 'number',
    value = 65,
)
n_input2 = dcc.Input(
    id = 'n_input2',
    type = 'number',
    value = 1,
)

### callbacks
def merge_cpd_dfs(df1, df2):
    # df1 more than df2, need to pad df2
    len1 = len(df1)
    len2 = len(df2)
    # if len1 > len2:
    #     print('len1 > len2')

    #     df2 = df2.append(df2.iloc[[-1] * (len1 - len2)]).reset_index(drop=True)
    #     print(len(df2))
    # elif len1 < len2:
    #     df1 = df1.append(df1.iloc[[-1] * (len2 - len1)]).reset_index(drop=True)
    
    merged_df = df1.merge(df2, on = 'Month', how = 'outer')
    merged_df = merged_df.round(2)
    return merged_df


def plot_merged_bar(df):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name = 'Amount_x1', x = df.Month, y = df.Amount_x
            # , text = df.Amount_x
            # , textposition = 'outside'
            )
    )
    fig.add_trace(
        go.Bar(
            name = 'Amount_x2', x = df.Month, y = df.Amount_y
            # , text=df.Amount_y
            # , textposition = 'outside'
            )
    )

    fig.update_layout(barmode = 'group', template = 'plotly_dark')
    fig.update_layout(
        title="Comparing Returns",
        title_x = 0.5,
        xaxis_title="Time Period",
        yaxis_title="Amount",
        # legend_title="",
        hovermode = 'x unified',
        # font=dict(
        #     family="Courier New, monospace",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y= -0.4,
        xanchor="right",
        x=1
    ))
    return fig


### function to update all bars
@app.callback(
    [
        Output('cpd_bar', 'figure'),
        Output('cpd_bar2', 'figure'),
        Output('merged_bar', 'figure'),
    ],
    [
        Input('principal_input', 'value'),
        Input(component_id='rate_input', component_property='value'),
        Input('time_input', 'value'),

        Input('con_input', 'value'),
        Input('type_con_input', 'value'),
        Input('start_con_input', 'value'),
        Input('stop_con_input', 'value'),
        Input('n_input', 'value'),

        Input('principal_input2', 'value'),
        Input(component_id='rate_input2', component_property='value'),
        Input('time_input2', 'value'),

        Input('con_input2', 'value'),
        Input('type_con_input2', 'value'),
        Input('start_con_input2', 'value'),
        Input('stop_con_input2', 'value'),
        Input('n_input2', 'value'),
    ],
    # prevent_initial_callback = True,
)
def update_bars(
    principal, rate, time, con, type_con, start_con, stop_con, n, 
    principal2, rate2, time2, con2, type_con2, start_con2, stop_con2, n2):
    # if null vals, dont update the graph
    parameters = [
        principal, rate, time, con, type_con, start_con, stop_con, n, 
        principal2, rate2, time2, con2, type_con2, start_con2, stop_con2, n2
        ]
    if None in parameters:
        raise dash.exceptions.PreventUpdate
    else:
        df1 = cpd_interest_v4_2(principal, rate, time, con, type_con, start_con, stop_con, n)
        fig1 = create_cpd_fig_v2(df1)

        df2 = cpd_interest_v4_2(principal2, rate2, time2, con2, type_con2, start_con2, stop_con2, n2)
        fig2 = create_cpd_fig_v2(df2)

        merged_df = merge_cpd_dfs(df1, df2)
        merged_fig = plot_merged_bar(merged_df)

        return [fig1, fig2, merged_fig]

### app layout and bigger components
def create_label_input_col(x_label, x_input):
    """
    Creates a dbc.Col() object for an Input and Label object that is used to change the bar graph.

    """
    col = dbc.Col(
        [
            x_label,
            x_input,
        ],
        width = 6,
        lg = {
            'size' : 3,
        },
        md = {
            'size' : 4,
        },
        sm = {
            'size' : 6,
        },
        xs = {
            'size' : 12,
        },
        style = {
            # 'border' : 'solid green',
            'outline' : '1px solid grey',
            # 'border' : '1px solid grey',
            'padding-top': '10px',
            'padding-bottom': '10px',
            'display':'flex',
            'flex-direction':'column',
            'align-items': 'center',
        }
    )

    return col

### row of inputs for first bar chart
input_label_row = dbc.Row(
        [
            create_label_input_col(principal_label, principal_input),
            create_label_input_col(rate_label, rate_input),
            create_label_input_col(time_label, time_input),
            create_label_input_col(n_label, n_input),

            create_label_input_col(con_label, con_input),
            create_label_input_col(type_con_label, type_con_input),
            create_label_input_col(start_con_label, start_con_input),
            create_label_input_col(stop_con_label, stop_con_input),
        ]
    )

bar_card = dbc.Card(
    [
        # dbc.CardHeader("Testing header"),
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
                        input_label_row,
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



### row of inputs for second bar chart
input_label_row2 = dbc.Row(
        [
            create_label_input_col(principal_label, principal_input2),
            create_label_input_col(rate_label, rate_input2),
            create_label_input_col(time_label, time_input2),
            create_label_input_col(n_label, n_input2),

            create_label_input_col(con_label, con_input2),
            create_label_input_col(type_con_label, type_con_input2),
            create_label_input_col(start_con_label, start_con_input2),
            create_label_input_col(stop_con_label, stop_con_input2),
        ]
    )
bar_card2 = dbc.Card(
    [
        dbc.CardHeader("Testing header"),
        dbc.CardBody(
            [
                html.H1('he'),
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
                        input_label_row2,
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

### merged bar card to compare the 2 bar charts
merged_bar_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Graph(id = 'merged_bar', figure = {}),
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
                            'The Compound Effect',
                            style= {
                                'textAlign': 'center',
                            }
                        ),
                    ],
                    style = {
                        # 'border': 'solid blue',
                    }
                ),
            ],
            style = {
                # 'border': 'solid green',
            },
        ),

        ### main components
        bar_card,
        bar_card2,
        merged_bar_card,
        html.Br(),



    ],
    style = {
        # 'border': 'solid red',
    },
    fluid = True,
)

app.layout = layout


if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = True)