# Data Libraries
import pandas as pd
import numpy as np
import datetime
import time

# Dash APP
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from components.navbar import navbar
from components.visualizations import *
from components.utils import *
from plotly import graph_objects as go


df = pd.read_csv(
    "marketing_data.csv", sep=",", index_col=[0])


# CSS files and links
external_stylesheets = [dbc.themes.BOOTSTRAP,  # adding the bootstrap inside the application
                        # importing the font to the navlinks
                        "https://fonts.googleapis.com/css2?family=Poppins&display=swap"
                        ]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                # It's what make the app be responsive;
                meta_tags=[
                    {
                        "name": "viewport",
                        "content": "width=device-width, initial-scale=1, maximum-scale=1",
                    }
                ])

# help to work with dynamic callbacks
app.config.suppress_callback_exceptions = True

# allow the app access local css and js scripts
app.css.config.serve_locally = True

server = app.server

# setting the title
app.title = 'Marketing Comparison'

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    # 'color': 'white',
    'padding': '15px',
    'height': '55px',
    'margin': '8px 0px'
}

tab_style = {
    'border': '1px solid #d6d6d6',
    #    'backgroundColor': '#119DFF',
    # 'color': 'white',
    'padding': '15px',
    'height': '55px',
    'margin': '8px 0px'
}

# dynamic app layout
app.layout = html.Div([
    # navbar,
    navbar(logo="assets/logo-placeholder.png", height="50px"),
    html.Div(id="df-sharing", style={"display": "none"}),
    html.Div(id="comparison-infos", children=["AS", 70, 1],
             style={"display": "none"}),

    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="tabs-styled-with-inline", value='tab-1',
                     children=[
                         dcc.Tab(label='Segments', value='tab-1',
                                 selected_style=tab_selected_style, style=tab_style),
                         dcc.Tab(label='SandBox', value='tab-2',
                                 selected_style=tab_selected_style, style=tab_style),
                         dcc.Tab(label='Orchestration', value='tab-3',
                                 selected_style=tab_selected_style, style=tab_style),
                     ])
        ], width=10, md=10, lg=6)
    ], className="row-center bottom32"),
    # container with all app content (dynamic)
    dbc.Container(id="tabs-content-inline",
                  style={"maxWidth": "1360px", "minHeight": "100vh"})

], id="singlearity-app", style={'overflow': 'hidden'})


tab1 = dbc.Row([
    dbc.Col([dcc.Graph(id="fig1-funnel", figure=funnel_chart())],
            width={"offset": 0, "size": 12},
            md={"offset": 1, "size": 10},
            lg={"offset": 0, "size": 8}, className="bottom40"),
    dbc.Col([dcc.Graph(id="fig1-bar")],
            width={"offset": 0, "size": 12},
            md={"offset": 1, "size": 10},
            lg={"offset": 0, "size": 4}, className="bottom40"),
    dbc.Col([html.Div("GROUPS WORTH PAYING ATTENTION TO", className="font-lg text-center"),
             html.Div(id="tab1-val",
                      className="width-100")],
            width={"offset": 0, "size": 12},
            md={"offset": 1, "size": 10},
            lg={"offset": 1, "size": 10}, className="bottom40")
])


tab2 = dbc.Row([
    dbc.Col([dcc.Graph(id="fig2-bar", figure=bar_chart_2(df))],
            width={"offset": 0, "size": 12},
            md={"offset": 1, "size": 10},
            lg={"offset": 0, "size": 8}, className="bottom40"),
    dbc.Col([dcc.Graph(id="fig2-bar-prod", figure=bar_chart_2_produc(df))],
            width={"offset": 0, "size": 12},
            md={"offset": 1, "size": 10},
            lg={"offset": 0, "size": 4}, className="bottom40"),
    dbc.Col([html.Div("GROUPS WORTH PAYING ATTENTION TO", className="font-lg text-center"),
             html.Div(id="tab2-val",
                      className="width-100")],
            width={"offset": 0, "size": 12},
            md={"offset": 1, "size": 10},
            lg={"offset": 1, "size": 10}, className="bottom40")
])


tab3 = dbc.Row([
    dbc.Col([html.Div(id="tab3-val",
                      className="width-100")],
            width={"offset": 0, "size": 12},
            md={"offset": 0, "size": 12},
            lg={"offset": 1, "size": 10},
            className="bottom40"),
    dbc.Col([dcc.Graph(id="fig3-bar1", figure=bar_chart_3_browser(df))],
            width={"offset": 0, "size": 12},
            md={"offset": 0, "size": 12},
            lg={"offset": 1, "size": 10}, className="bottom40"),
    dbc.Col([dcc.Graph(id="fig3-sunburst", figure=sunburst(df))],
            width={"offset": 0, "size": 12},
            md={"offset": 2, "size": 8},
            lg={"offset": 0, "size": 6}, className="bottom40"),
    dbc.Col([dcc.Graph(id="fig3-bar2", figure=bar_chart_2(df))],
            width={"offset": 0, "size": 12},
            md={"offset": 2, "size": 8},
            lg={"offset": 0, "size": 6}, className="bottom40")


])


@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])
def render_content(tab):

    if tab == 'tab-1':
        return tab1

    elif tab == 'tab-2':
        return tab2

    elif tab == 'tab-3':
        return tab3


@app.callback(Output('df-sharing', 'children'),
              [Input('tabs-styled-with-inline', 'children')])
def render_tab(hover):

    df = pd.read_csv(
        "marketing_data.csv", sep=",", index_col=[0])

    return df.to_json(date_format='iso', orient='split')


@app.callback(Output('tab1-val', 'children'),
              [Input("df-sharing", "children"),
               Input('fig1-funnel', 'hoverData')])
def render_tab(data, hover):
    df = pd.read_json(data, orient='split')

    if hover is None:
        df = df
    elif hover['points'][0]['y'] == "All":
        df = df
    else:
        filt = hover['points'][0]['y']
        df = df[df["Funnel"] == filt]

    # print(df.head())
    table = table_show(df)

    return table


@app.callback(Output('fig1-bar', 'figure'),
              [Input("df-sharing", "children"),
               Input('fig1-funnel', 'hoverData')])
def render_bar(data, hover):
    df = pd.read_json(data, orient='split')

    if hover is None:
        df = df
    elif hover['points'][0]['y'] == "All":
        df = df
    else:
        filt = hover['points'][0]['y']
        df = df[df["Funnel"] == filt]

    # print(filt)
    bar_fig = bar_chart(df)

    return bar_fig


@app.callback(Output('tab2-val', 'children'),
              [Input("df-sharing", "children")])
def render_tab(data):

    df = pd.read_json(data, orient='split')

    # print(df.head())
    table = table_show(df)

    return table


@app.callback(Output('tab3-val', 'children'),
              [Input("df-sharing", "children")])
def render_tab(data):

    df = pd.read_json(data, orient='split')

    # print(df.head())
    table = table_show(df)

    return table


@ app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
