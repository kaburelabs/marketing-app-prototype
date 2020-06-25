
from plotly import graph_objects as go
import pandas as pd
import dash_html_components as html
import dash_table as dt
import plotly_express as px


df = pd.read_csv(
    "marketing_data.csv", sep=",", index_col=[0])


def funnel_chart():

    tmp = df["Funnel"].value_counts().reset_index()

    df2 = pd.DataFrame({"index": ["All"],
                        "Funnel": [tmp["Funnel"].sum()]})
    tmp = tmp.append(df2, ignore_index=True, sort=True)
    tmp.sort_values("Funnel", ascending=False, inplace=True)

    fig = go.Figure(go.Funnel(

        y=tmp['index'],
        x=tmp['Funnel'],
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
    x, y = tmp['index'], tmp['Products']

    # Use textposition='auto' for direct text
    fig = go.Figure(data=[go.Bar(
        x=x.values, y=y.values,
        text=y,
        textposition='auto',
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
        style_table={'minHeight': '330px', "maxHeight": "330px",
                     'textAlign': "left",
                     "maxWidth": "1360px", },
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'minWidth': '150px', 'maxWidth': '280px',
                'textAlign': "left"
            } for c in ['Company Name', 'email', 'phone', 'SocialMedia', "Costs"]],
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

    fig = px.bar(tmp, x='index', y="Products",
                 barmode="group", title="PRODUCTS")

    fig.update_layout(title_x=.5, margin=dict(t=50))

    return fig


def bar_chart_3_browser(df):

    tmp = df.groupby(["Funnel", 'SocialMedia'])['email'].count().reset_index()

    fig = px.bar(tmp, x='SocialMedia', y="email", color="Funnel",
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
