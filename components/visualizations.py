
from plotly import graph_objects as go
import pandas as pd
from dash import dash_table as dt, html, dcc
import plotly.express as px


df = pd.read_csv(
    "marketing_data.csv", sep=",", index_col=[0])


def funnel_chart():

    tmp = df["Funnel"].value_counts().reset_index()

    df2 = pd.DataFrame({"Funnel": ["All"],
                        "count": [tmp["count"].sum()]})
    tmp = pd.concat([tmp, df2], ignore_index=True) 
    tmp.sort_values("count", ascending=False, inplace=True)

    fig = go.Figure(go.Funnel(

        y=tmp['Funnel'],
        x=tmp['count'],
        textposition="inside",
        textinfo="value+percent initial",
        opacity=0.65, marker={"color": ["deepskyblue", "lightsalmon", "tan", "teal"],
                              "line": {"width": [4, 2, 3, 1], "color": ["wheat", "blue", "wheat", "wheat"]}},
        connector={"line": {"color": "royalblue", "dash": "dot", "width": 3}})
    )
    fig.update_layout(title="CORE CUSTOMER LOOKALIKE PROFILES",
                      title_x=.5, margin=dict(t=50))
    return fig


def bar_chart(df):

    tmp = df['Products'].value_counts().sort_index().reset_index()
    x, y = tmp['count'], tmp['Products']

    # Use textposition='auto' for direct text
    fig = go.Figure(data=[go.Bar(
        x=x, y=y,
        text=y,
        textposition='auto',
        orientation='h'
    )])

    fig.update_layout(title="ALERTS",
                      title_x=.5, margin=dict(t=50))
    return fig


def table_show(df):

    table = dt.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c}
                 for c in ["Company Name", "email", "phone", "SocialMedia", "Costs", "Customer Address"]],
        page_size=10,
        style_table={'minHeight': '330px', 
                     "maxHeight": "330px",
                     'textAlign': "left",
                     'width': '100%',
                     "maxWidth": "1360px", },
        # style_cell_conditional=[
            # {
            #     'if': {'column_id': c},
            #     'minWidth': '150px', 'maxWidth': '280px',
            #     'textAlign': "left"
            # } for c in ['Company Name', 'email', 'phone', 'SocialMedia', "Costs"]],
        style_as_list_view=True,
    )

    return table


def bar_chart_2(df):

    fig = px.bar(df, y='Priority', x="Costs",
                 color='Campaing', barmode="group", orientation="h", title="POWER BI DASHBOARD")

    fig.update_layout(title_x=.5, margin=dict(t=50))

    return fig


def bar_chart_2_produc(df):

    tmp = df['Products'].value_counts().sort_index().reset_index()

    fig = px.bar(tmp, x=tmp.index, y="Products",
                 barmode="group", title="PRODUCTS")

    fig.update_layout(title_x=.5, margin=dict(t=50))

    return fig


def bar_chart_3_browser(df):

    tmp = df.groupby(["Funnel", 'SocialMedia'])['email'].count().reset_index()

    fig = px.bar(tmp, x=tmp.index, y="email", color="Funnel",
                 barmode="group", title="REACHABILITY")

    fig.update_layout(title_x=.5, margin=dict(t=50))

    return fig


def sunburst(df):

    fig = px.sunburst(df, path=['Funnel', 'SocialMedia', 'Priority',
                                "Products"], values='Costs',
                      title="Lead Cost Details <br> (Click to go in depth)",
                      maxdepth=2)

    fig.update_layout(title_x=.5, margin=dict(t=70, b=0, r=0, l=0))

    return fig
