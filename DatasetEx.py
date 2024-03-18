# import pandas for initial exploration of dataset
import pandas as pd
# import plotly for graph
import plotly.graph_objects as go
# USING DASH!
import dash

from dash import dcc
from dash import html

print(pd.__version__) # print version in case something breaks later on

# Import the data as a df simply with read_csv from pandas package
df = pd.read_csv('AnalysisData.csv')

# multi_plot requires two variables:

fig = go.Figure()

for column in df.columns.drop(['Operator', 'Reservoir', 'CompletionDate']).to_list():
    fig.add_trace(
        go.Scatter(
            x = df.index,
            y = df[column],
            name = column
        )
    )

def create_layout_button(column):
    return dict(label = column,
                method = 'update',
                args = [{'visible': df.columns.drop(['Operator', 'Reservoir', 'CompletionDate']).isin([column]),
                         'title': column,
                         'showlegend': True}])

fig.update_layout(
    updatemenus=[go.layout.Updatemenu(
        active = 4,
        buttons = list(df.columns.drop(['Operator', 'Reservoir', 'CompletionDate']).map(lambda column: create_layout_button(column)))
        )
    ])

fig.show()

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])
app.run_server(debug=True, port=1010)