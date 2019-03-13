import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_with_codes.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Demographic data by country")
    ], style={
        'textAlign': "center",
        "padding-bottom": "30"}),
    html.Div([
        dcc.Dropdown(id="value-selected",
                     options=[{'label': "Population", 'value': 'pop'},
                              {'label': "GDP Per Capita", 'value': 'gdpPercap'},
                              {'label': "Life Expectancy", 'value': 'lifeExp'}],
                     value='lifeExp',
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "70%"

                     }
                     )
    ]),
    dcc.Graph(id="my-graph")

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")]
)
def update_figure(selected):
    dff = df.groupby(['iso_alpha', 'country']).mean().reset_index()

    def title(text):
        if text == "pop":
            return "Poplulation"
        elif text == "gdpPercap":
            return "GDP Per Capita"
        else:
            return "Life Expectancy"

    trace = go.Choropleth(
        locations=dff['iso_alpha'],
        z=dff[selected],
        text=dff['country'],
        autocolorscale=False,
        colorscale="YlGnBu",
        marker={'line': {'color': 'rgb(180,180,180)',
                         'width': 0.5}},
        colorbar={"thickness": 10,
                  "len": 0.3,
                  "x": 0.9,
                  "y": 0.7,
                  'title': {"text": title(selected), "side": "bottom"}}
    )
    return {
        "data": [trace],
        "layout": go.Layout(
            title=title(selected),
            height=800,
            geo={'showframe': False,
                 'showcoastlines': False,
                 'projection': {'type': "miller"}}
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# TODO: Change podition of colorbar
 # cant be horizontal.
