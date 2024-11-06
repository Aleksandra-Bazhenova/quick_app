import pandas as pd
import numpy as np
import plotly.graph_objects as go


from dash import dash_table, dcc, html, ALL, ctx
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Input, Output, State, Dash, Trigger, FileSystemCache

external_stylesheets = [dbc.themes.SKETCHY]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True,
    )

server = app.server

co_occurrence_df = pd.read_csv('src/azure - co_occurrence_df.csv', index_col=0)
co_occurrence_dict = pd.Series(co_occurrence_df['Count'].values, index=co_occurrence_df['Pair']).to_dict()
alert_pairs = [pair.split(';') for pair in co_occurrence_dict.keys()]
unique_alerts = sorted(set(alert for sublist in alert_pairs for alert in sublist))
co_occurrence_matrix = pd.DataFrame(np.zeros((len(unique_alerts), len(unique_alerts))), index=unique_alerts, columns=unique_alerts)

for pair, count in co_occurrence_dict.items():
    first, second = pair.split(';')
    co_occurrence_matrix.loc[first, second] = count
    co_occurrence_matrix.loc[second, first] = count
    
fig = go.Figure(data=go.Heatmap(
                    z=co_occurrence_matrix.values,
                    x=unique_alerts,
                    y=unique_alerts,
                    colorscale='Turbo',
                    hoverongaps=False))

fig.update_layout(
    title='Alert Temporal Proximity Matrix',
    xaxis=dict(tickmode='array', tickvals=list(range(len(unique_alerts))), ticktext=unique_alerts),
    yaxis=dict(tickmode='array', tickvals=list(range(len(unique_alerts))), ticktext=unique_alerts),
    autosize=True,
    width=2000,
    height=2000
)

fig.update_xaxes(tickangle=-90)

app.layout = dbc.Container(
    [
    dbc.Row(
        html.Div(
            children=[],
            style={
                'textAlign': 'center',
                'color': 'white',
                'backgroundColor': '#003B5C'
                }
            )
        ),
    dcc.Graph(
        id='graph-content',
        figure=fig,
        style={'height': '600px', 'width': '600px'}
        )
    ],
    style={'padding': '30px 100px 30px 100px'},
    fluid=True
    )

if __name__ == '__main__':
    app.run(debug=True)

