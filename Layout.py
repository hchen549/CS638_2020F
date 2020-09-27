import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

import numpy as np
from dash.dependencies import Input, Output
import pandas as pd
import xlrd

app = dash.Dash()


df = pd.read_csv("final.csv")
state_policy = pd.read_csv("state_policy.csv")

CARD_KEYS = ['retail', 'grocery', 'parks', 'transit', 'workplaces', 'residential']

# the layout of the correlation page
correlation_layout = html.Div(children=[
        dcc.Dropdown(
            id='state-dropdown',
            options=
                [{"label": state, "value": state} for state in df.county.unique()]
            ,
            value='Dane',
            clearable=False,
            style={"width": 100}
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([], id=key+'_card') for key in CARD_KEYS
            ],
            className="mb-4",
        ),

        html.H3(
            'Daily Confirmed Cases',
            style={'text-align': 'center'}
        ),
        dcc.Graph(
            id='line_chart',
            style={
                'width': '80%',
                'height': '500px',
                'text-align': 'center',
                'margin': 'auto'
            }
        ),
        html.H3(
            'Percentage of Change in Mobility',
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Dropdown(
                id='type-dropdown',
                options=
                    [{"label": type, "value": type} for type in CARD_KEYS]
                ,
                value='retail',
                clearable=False,
                style={"width": 100}
        ),dcc.Graph(
            id='trend_chart',
            style={
                'width': '80%',
                'height': '500px',
                'text-align': 'center',
                'margin': 'auto'
            }
        )
        ])
])

@app.callback(
     Output('trend_chart', 'figure'),
    [Input('state-dropdown', 'value'),
     Input("type-dropdown",'value')])
def display_line_chart(value, type):
    state_df = df.loc[df.county==value].copy()

    fig = px.scatter(state_df, x="date", y=type)
    return fig

@app.callback(
    Output('line_chart', 'figure'),
    [Input('state-dropdown', 'value')])
def display_line_chart(value):
    state_df = df.loc[df.county==value].copy()
    fig = px.line(state_df, x='date', y='new_cases')
    # for i in range(len(state_policy)):
    #     if state_policy["Type"][i] == "Government":
    #         line_color = "navy"
    #     else:
    #         line_color = "Crimson"
    #
    #     fig.add_trace(go.Scatter(x=[state_policy["date"][i],
    #                                 state_policy["date"][i]],
    #                              y=[-300, 10000],
    #                              mode="lines",
    #                              name="SIGNAL",
    #                              hovertext=state_policy["response"][i],
    #                              marker=dict(size=12,
    #                                          line=dict(width=0.8),
    #                                          color=line_color
    #                                          ),
    #                              visible=True
    #                              ))
    return fig

@app.callback(
    [Output(key +'_card', 'children') for key in CARD_KEYS],
    [Input('state-dropdown', 'value')])
def update_card_value(value):
    state_df = df.loc[df.county==value].copy()
    correlations = state_df.corr().loc[CARD_KEYS, 'new_cases']
    return [dbc.Card(dbc.CardBody(
        [
            html.H5(key.title(), className="card-title"),
            html.P("Correlation: " + str(correlations[key]), className="card-text",
            ),
        ]
    ), color="danger" if correlations[key] < 0 else "success") for key in CARD_KEYS]


CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div([ html.Div(id="page-content",children=correlation_layout, style=CONTENT_STYLE)])

if __name__ == '__main__':
    app.run_server(port=4050)
