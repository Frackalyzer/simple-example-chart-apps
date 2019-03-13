import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Mining-BTC-180.csv')
df["month"] = pd.DatetimeIndex(df["Date"]).month

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Bitcoin statistics over time"),
        html.A("CSV-Dataset", href="https://raw.githubusercontent.com/plotly/datasets/master/Mining-BTC-180.csv",
               target="_blank")
    ], style={
        'textAlign': "center"}),
    html.Div([
        dcc.Dropdown(
            id='value-selected',
            options=[{'label': i, 'value': i} for i in df.columns.values[2:9]],
            value=["Number-transactions"],
            multi=True,
            style={
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
                "width": "80%"

            }

        )
    ]),
    dcc.Graph(id="my-graph"),
    html.Div([
        dcc.RangeSlider(
            id='month-selected',
            min=4,
            max=10,
            step=1,
            marks={
                4: "April",
                5: "May",
                6: "June",
                7: "July",
                8: "August",
                9: "September",
                10: "October"

            },
            value=[5, 7]
        )
    ])

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("month-selected", "value"),
     dash.dependencies.Input("value-selected", "value")]
)
def update_graph(selected1, selected2):
    dff = df[(df["month"] >= selected1[0]) & (df["month"] <= selected1[1])]

    trace = []
    for indicator in selected2:
        trace.append(go.Scatter(
            x=dff.Date,
            y=dff[indicator],
            name=indicator,
            mode="lines",
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'}
            },
        ))

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"{','.join(str(i) for i in selected2)} vs Date",
            xaxis={
                "title": "Date"
            },
            yaxis={
                "title": f"{','.join(str(i) for i in selected2)}"
            }

        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# TODO: adjust the title list
