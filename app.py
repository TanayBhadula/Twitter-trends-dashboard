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
                html.P(children="🐰", className="header-emoji"),
                html.H1(
                    children="Twitter Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the current twitter trends country wise ",
                    className="header-description",
                ),
                html.P(
                    children="Made with ❤️ by Tanay Bhadula",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Country", className="menu-title"),
                        dcc.Dropdown(
                            id="country-filter",
                            options=[
                                {"label": country, "value": country}
                                for country in np.sort(data.country.unique())
                            ],
                            value="Worldwide",
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
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="pie-chart", config={"displayModeBar": False},
                    ),
                    className="card2",
                ),
                
            ],
            className="wrapper2",
        ),
    ]
)



@app.callback(
    [Output("trend-chart", "figure"),
    Output("pie-chart", "figure")],
    
    [
        Input("country-filter", "value")
    ],
)
def update_charts(country):
    mask = (
        (data.country == country)
    )

    filtered_data = data.loc[mask, :]
    fig = px.bar(data[mask], x='name', y='tweet_volume',
    hover_data=['tweet_volume', 'url'], color='tweet_volume',
             labels={'tweet_volume':'Tweet Volume'}, height=400)

    fig2 = px.pie(data[mask], values='tweet_volume', names='name', title='Trending in various countries')
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(margin=dict(t=40, b=5, l=5, r=5))


    return fig,fig2

 
if __name__ == "__main__":
    app.run_server(debug=True)