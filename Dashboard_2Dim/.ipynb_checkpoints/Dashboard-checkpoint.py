import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

stylesheets = ['bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=stylesheets)

df = pd.read_csv('../AnalysisData.csv')
# Indicators that can be selected by dropdowns only float 
available_indicators = list(df.columns.drop(['Operator', 'Reservoir', 'CompletionDate','rowID']))

#transform every unique date to a number
df['CompletionDate'] = pd.to_datetime(df['CompletionDate'], format='%m/%d/%Y')
df['CompletionYear'] = pd.DatetimeIndex(df['CompletionDate']).year

color_discrete_map = {'WOLFCAMP A': 'rgb(0,0,255)', 
                      'WOLFCAMP B': 'rgb(100, 149, 237)',
                      'WOLFCAMP C': 'rgb(0, 150, 255)',
                      'WOLFCAMP D': 'rgb(0, 128, 128)', #teal
                      'DEAN': 'rgb(233, 116, 81)', #burnt siena
                      'SPRABERRY UPPER': 'rgb(255, 68, 51)',
                      'SPRABERRY MIDDLE': 'rgb(175, 225, 175)',
                      'SPRABERRY LOWER SHALE': 'rgb(255, 192, 0)', 
                      'SPRABERRY LOWER': 'rgb(170, 255, 0)',
                     }

app.layout = html.Div([

    # adding the dropdowns for x, y selection
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter_xaxis_column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='TotalWellCost_USDMM'
            ),
            dcc.RadioItems(
                id='crossfilter_xaxis_type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter_yaxis_column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='CumOil12Month'
            ),
            dcc.RadioItems(
                id='crossfilter_yaxis_type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'padding': '10px 5px'
    }),

    # adding the Graphs
    #     scatter cumulative year value
    html.Div([
        dcc.Graph(
            id='crossfilter_indicator_scatter_cumul',
            hoverData={'points': [{'customdata': 'OXY'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '5px'}),
    
    #     scatter single year value
    html.Div([
        dcc.Graph(
            id='crossfilter_indicator_scatter',
            hoverData={'points': [{'customdata': 'OXY'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '5px'}),

    #then in the Slider for time series control
    html.Div(dcc.Slider(
        id='crossfilter_date_slider',
        min=df['CompletionYear'].min(),
        max=df['CompletionYear'].max(),
        value=df['CompletionYear'].max(),
        marks={str(year): str(year) for year in df['CompletionYear'].unique()},
        step=None
            ), style={'width': '90%', 'padding': '0px 20px 20px 20px'}),
    
    #     hist x values CUMULATIVE
    html.Div([
        dcc.Graph(
            id='crossfilter_indicator_xhist_cum'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '5px'}),

    #     hist x values SINGLE YEAR
    html.Div([
        dcc.Graph(
            id='crossfilter_indicator_xhist'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '5px'}),

    #     hist y values CUMULATIVE
    html.Div([
        dcc.Graph(
            id='crossfilter_indicator_yhist_cum'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '5px'}),
    
    #     hist y values SINGLE YEAR
    html.Div([
        dcc.Graph(
            id='crossfilter_indicator_yhist'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '5px'}),
# end of major DIV   
])


@app.callback(
    dash.dependencies.Output('crossfilter_indicator_scatter_cumul', 'figure'),
    [dash.dependencies.Input('crossfilter_xaxis_column', 'value'),
     dash.dependencies.Input('crossfilter_yaxis_column', 'value'),
     dash.dependencies.Input('crossfilter_xaxis_type', 'value'),
     dash.dependencies.Input('crossfilter_yaxis_type', 'value'),
     dash.dependencies.Input('crossfilter_date_slider', 'value')])
def update_graph_cumul(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff_1 = df[df['CompletionYear'] <= year_value]

    fig_1 = px.scatter(dff_1, x=xaxis_column_name,
                       y=yaxis_column_name,
                       height = 750,
                       hover_name='rowID',
                       color='Reservoir',
                       color_discrete_map=color_discrete_map,
                       symbol='Reservoir'  #added
                      )

    fig_1.update_traces(customdata=dff_1['Operator'],
                      marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    fig_1.update_xaxes(title=xaxis_column_name+' up to '+str(year_value), type='linear' if xaxis_type == 'Linear' else 'log', side= 'top' )

    fig_1.update_yaxes(title=yaxis_column_name+' up to '+str(year_value), type='linear' if yaxis_type == 'Linear' else 'log')
       
    fig_1.update_layout(margin={'l': 100, 'b': 100, 't': 20, 'r': 10}, hovermode='closest',
                      paper_bgcolor='rgba(0,0,0,0)',
                      #plot_bgcolor='rgba(188, 188, 188, 0.8)',
                      legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=-0.15,
                                  xanchor="right",
                                  x=1
                                 ))
    
    return fig_1

@app.callback(
    dash.dependencies.Output('crossfilter_indicator_scatter', 'figure'),
    [dash.dependencies.Input('crossfilter_xaxis_column', 'value'),
     dash.dependencies.Input('crossfilter_yaxis_column', 'value'),
     dash.dependencies.Input('crossfilter_xaxis_type', 'value'),
     dash.dependencies.Input('crossfilter_yaxis_type', 'value'),
     dash.dependencies.Input('crossfilter_date_slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff_2 = df[df['CompletionYear'] == year_value]
    
    fig_2 = px.scatter(dff_2, x=xaxis_column_name,
                       y=yaxis_column_name,
                       height = 750,
                       hover_name='rowID',
                       color='Operator',
                       symbol='Operator'  #added
                      )

    fig_2.update_traces(customdata=dff_2['Operator'],
                      marker=dict(size=12,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                                        selector=dict(mode='markers'))

    fig_2.update_xaxes(title=xaxis_column_name+' for '+str(year_value), type='linear' if xaxis_type == 'Linear' else 'log', side= 'top')

    fig_2.update_yaxes(title=yaxis_column_name+' for '+str(year_value), type='linear' if yaxis_type == 'Linear' else 'log')
   
    fig_2.update_layout(margin={'l': 100, 'b': 100, 't': 20, 'r': 10}, hovermode='closest',
                      paper_bgcolor='rgba(0,0,0,0)',
                      #plot_bgcolor='rgba(188, 188, 188, 0.8)',
                      legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=-0.15,
                                  xanchor="right",
                                  x=1
                                 ))

    return fig_2

# HISTOGRAM X AXIS values CUMULATIVE
@app.callback(
    dash.dependencies.Output('crossfilter_indicator_xhist_cum', 'figure'),
    [dash.dependencies.Input('crossfilter_xaxis_column', 'value'),
     dash.dependencies.Input('crossfilter_date_slider', 'value')])
def update_xhist(xaxis_column_name,
                 year_value):
    dff_1 = df[df['CompletionYear'] <= year_value]

    fig_3 = px.histogram(dff_1, x=xaxis_column_name,
                       nbins=30,
                       color='Reservoir',
                       color_discrete_map=color_discrete_map,
                      )

    fig_3.update_xaxes(title=xaxis_column_name+' up to '+str(year_value))
  
    fig_3.update_layout(margin={'l': 100, 'b': 100, 't': 20, 'r': 10})

    return fig_3

# HISTOGRAM Y AXIS values CUMULATIVE
@app.callback(
    dash.dependencies.Output('crossfilter_indicator_yhist_cum', 'figure'),
    [dash.dependencies.Input('crossfilter_yaxis_column', 'value'),
     dash.dependencies.Input('crossfilter_date_slider', 'value')])
def update_yhist(yaxis_column_name,
                 year_value):
    dff_1 = df[df['CompletionYear'] <= year_value]

    fig_4 = px.histogram(dff_1, x=yaxis_column_name,
                       nbins=30,
                       color='Reservoir',
                       color_discrete_map=color_discrete_map,
                      )
    
    fig_4.update_xaxes(title=yaxis_column_name+' up to '+str(year_value))
  
    fig_4.update_layout(margin={'l': 100, 'b': 100, 't': 20, 'r': 10})

    return fig_4


# HISTOGRAM X AXIS values
@app.callback(
    dash.dependencies.Output('crossfilter_indicator_xhist', 'figure'),
    [dash.dependencies.Input('crossfilter_xaxis_column', 'value'),
     dash.dependencies.Input('crossfilter_date_slider', 'value')])
def update_xhist(xaxis_column_name,
                 year_value):
    dff_2 = df[df['CompletionYear'] == year_value]

    fig_3 = px.histogram(dff_2, x=xaxis_column_name,
                       nbins=30,
                       color='Operator'
                      )

    fig_3.update_xaxes(title=xaxis_column_name+' for '+str(year_value))
  
    fig_3.update_layout(margin={'l': 100, 'b': 100, 't': 20, 'r': 10})

    return fig_3

# HISTOGRAM Y AXIS values
@app.callback(
    dash.dependencies.Output('crossfilter_indicator_yhist', 'figure'),
    [dash.dependencies.Input('crossfilter_yaxis_column', 'value'),
     dash.dependencies.Input('crossfilter_date_slider', 'value')])
def update_yhist(yaxis_column_name,
                 year_value):
    dff_2 = df[df['CompletionYear'] == year_value]

    fig_6 = px.histogram(dff_2, x=yaxis_column_name,
                       nbins=30,
                       color='Operator'
                      )
    
    fig_6.update_xaxes(title=yaxis_column_name+' for '+str(year_value))
  
    fig_6.update_layout(margin={'l': 100, 'b': 100, 't': 20, 'r': 10})

    return fig_6


if __name__ == '__main__':
    app.run_server(port=8000, debug = True, use_reloader=False)