import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Network Graph")

    ], className="row", style={
        'textAlign': "center"
    }),
    html.Div([
        html.Span("Number of nodes : ", className="six columns", style={"text-align": "right"}),
        dcc.RadioItems(
            id='nodes',
            options=[{'label': i, 'value': i} for i in [30, 50, 80, 100]],
            value=80,
            labelStyle={'display': 'inline-block', "padding-left": 5,"padding-right": 5},
            className="six columns"
        )
    ], className="row",
        style={"margin-right": "auto", "margin-left": "auto", "display": "block", "width": "80%", "padding": 20}),
    html.Div([
        dcc.Graph(id="my-graph", )]),

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("nodes", "value")]
)
def update_graph(n):
    G = nx.random_geometric_graph(n, 0.15)

    pos = nx.get_node_attributes(G, 'pos')

    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line={'width': 0.5, 'color': '#888'},
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker={'showscale': True,
                'colorscale': 'Jet',
                'reversescale': True,
                'color': [], 'size': 10,
                'colorbar': {'thickness': 10, 'title': 'No of Connections', 'xanchor': 'left', 'titleside': 'right'},
                'line': {'width': 2}})

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
    p = nx.single_source_shortest_path_length(G, ncenter)

    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_info = 'Number of connections: ' + str(len(adjacencies[1]))
        node_trace['text'] += tuple([node_info])

    figure = {
        "data": [edge_trace, node_trace],
        "layout": go.Layout(
            title='Network Graph With Dash',
            showlegend=False,
            hovermode='closest',
            margin={'b': 20, 'l': 5, 'r': 5, 't': 40},
            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False})
    }

    return figure


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)