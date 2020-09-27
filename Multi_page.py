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
homepage_layout = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Markdown([
                                "##### Mobility Types\n",
                                "**Grocery & pharmacy**\n",
                                "Mobility trends for places like grocery markets, food warehouses, \
                                    farmers markets, specialty food shops, drug stores, and pharmacies.\n",
                                "**Parks**\n",
                                "Mobility trends for places like local parks, national parks, public beaches,\
                                    marinas, dog parks, plazas, and public gardens.\n",
                                "**Transit stations**\n",
                                "Mobility trends for places like public transport hubs such as subway, bus, and train stations.\n",
                                "**Retail & recreation**\n",
                                "Mobility trends for places like restaurants, cafes, shopping centers, \
                                    theme parks, museums, libraries, and movie theaters.\n",
                                "**Residential**\n", "Mobility trends for places of residence.\n",
                                "**Workplaces**\n", "Mobility trends for places of work."

                            ])),
                            dbc.Col(dcc.Markdown([
                                "##### Correlation Coefficients between Daily Cases and Mobility\n",
                                "It is the number that describes how people reacted to the reported daily cases "\
                                    "in the previous days. It takes values between -1 and 1. A positive value indicates that "\
                                        "as the reported daily cases increased, people's mobility decreased in the following day.\n",
                                "##### Data resources\n",
                                "[Google COVID-19 Community Mobility Reports](https://www.google.com/covid19/mobility/index.html?hl=en)\n",
                                "[John Hopkins Daily Reports](https://github.com/CSSEGISandData/COVID-19)\n",
                                "[New York Times COVID-19 Reports](https://github.com/nytimes/covid-19-data)"
                            ])),
                        ]
                    )
                ]
)


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
                dbc.Col([], id=key+'_card', width=2) for key in CARD_KEYS
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
            ), dcc.Graph(
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
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# save all the parameters of the pages for easy accessing
PAGES = [
    {'children': 'Home', 'href': '/', 'id': 'home'},
    {'children': 'Correlation', 'href': '/correlation', 'id': 'correlation-page'}
]

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
                dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
                dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
# the layout of the sidebar
sidebar_layout = html.Div(
    [
        html.Div([
                    dbc.Row([html.H4("CS638")
                            ])
                    ]),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", id="home")
            ],
            vertical=False,
            pills=True,
        ),
        dbc.Nav(
            [
                dbc.NavLink("Week 09/28", href="/correlation", id="correlation-page")
            ],
            vertical=False,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
)

app.layout = html.Div([ dcc.Location(id="url"), sidebar_layout,
#                     dcc.Link('Navigate to "/"', href='/'),
    #                     html.Br(),
    #                     dcc.Link('Navigate to "/page-2"', href='/page-2'),
    # dcc.Location(id='url', refresh=False),
    #                     dcc.Link('Navigate to "/"', href='/'),
    #                     html.Br(),
    #                     dcc.Link('Navigate to "/page-2"', href='/page-2'),
                        html.Div(id="page-content", style=CONTENT_STYLE)])

# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     return correlation_layout


@app.callback(Output("page-content", "children"),
             [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/':
        return homepage_layout
    elif pathname == "/correlation":
        return correlation_layout

if __name__ == '__main__':
    app.run_server(port=4050, debug=False)