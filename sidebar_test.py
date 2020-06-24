import dash_html_components as html
import dash_trich_components as dtc
from dash.dependencies import Input, Output
import pandas as pd

content_1 = html.Div('content 1')
content_2 = html.Div('content 2')
content_3 = html.Div('content 3')
content_4 = html.Div('content 4')
content_5 = html.Div('content 5')

app.layout = html.Div([
    dtc.SideBar([
        dtc.SideBarItem(id='id_1', label="Label 1", icon="fas fa-home"),
        dtc.SideBarItem(id='id_2', label="Label 2", icon="fas fa-chart-line"),
        dtc.SideBarItem(id='id_3', label="Label 3", icon="far fa-list-alt"),
        dtc.SideBarItem(id='id_4', label="Label 4", icon="fas fa-info-circle"),
        dtc.SideBarItem(id='id_5', label="Label 5", icon="fas fa-cog"),
    ]),
    html.Div(id="page_content")
])


@app.callback(
    Output("page_content", "children"),
    [
        Input("id_1", "n_clicks_timestamp"),
        Input("id_2", "n_clicks_timestamp"),
        Input("id_3", "n_clicks_timestamp"),
        Input("id_4", "n_clicks_timestamp"),
        Input("id_5", "n_clicks_timestamp")
    ]
)
def toggle_collapse(input1, input2, input3, input4, input5):
    btn_df = pd.DataFrame({"input1": [input1], "input2": [input2],
                           "input3": [input3], "input4": [input4],
                           "input5": [input5]})

    btn_df = btn_df.fillna(0)

    if btn_df.idxmax(axis=1).values == "input1":
        return content_1
    if btn_df.idxmax(axis=1).values == "input2":
        return content_2
    if btn_df.idxmax(axis=1).values == "input3":
        return content_3
    if btn_df.idxmax(axis=1).values == "input4":
        return content_4
    if btn_df.idxmax(axis=1).values == "input5":
        return content_5


if __name__ == '__main__':
    app.run_server(debug=True)
