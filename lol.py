import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd


data = pd.read_csv("merged.csv")
#data = df.query("country == 'Canada'")
#data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("tweet_volume", inplace=True)

#country = data.country.unique()

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Twitter Trends Analytics!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Twitter Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in np.sort(data.country.unique())
                            ],
                            value="Canada",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                
                
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="trend-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                
            ],
            className="wrapper",
        ),
    ]
)



@app.callback(
    Output("trend-chart", "figure"),
    
    [
        Input("country-filter", "value")
    ],
)
def update_charts(country):
    mask = (
        (data.country == country)
    )

    filtered_data = data.loc[mask, :]
    trend_chart_figure = {
        "data": [
            {
                "x": filtered_data["name"],
                "y": filtered_data["tweet_volume"],
                "type": "bar-chart",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return trend_chart_figure

 
if __name__ == "__main__":
    app.run_server(debug=True)