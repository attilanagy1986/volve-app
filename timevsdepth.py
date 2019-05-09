import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

from app import app
import data_extraction

#function to create the time/depth plot
def timevsdepth_plot(df):

    trace0 = go.Scatter(
        x=df['Time'],
        y=[0 for num in df.index],
        mode='markers',
        marker = dict(
            color = 'rgb(0,0,0)',
            size = 0.1,
            ),
        name='dummy_data',
        hoverinfo='none',
        showlegend=False,
    )

    trace1 = go.Scatter(
        x=df['Time'],
        y=df['MD (m)'],
        mode='lines+markers',
        line = dict(
            color = ('rgb(7,178,178)'),
            width = 2
            ),
        marker = dict(
            color = 'rgb(7,178,178)',
            size = 5,
            ),
        name='MD',
        text=[
            "<b>Date:</b> {}<br>"
            "<b>MD:</b> {} m<br>"
            "<b>Section:</b> {} in<br>"
            "<b>Summary:</b> {}"
            .format(
                str(df['Time'].loc[num])[0:10],
                df['MD (m)'].loc[num],
                df['Section (in)'].loc[num],
                df['Summary'].loc[num].replace('.','<br>')
            )
            for num in df.index
        ],
        hoverinfo="text",
        hoverlabel=dict(
            bgcolor='rgb(255,255,255)',
            bordercolor='rgb(0,0,0)'
        ),
        showlegend=False,
    )

    data = [trace0,trace1]

    layout = go.Layout(
        title=None,
        xaxis=dict(
            title=dict(
                text='<b>Days</b>',
                font=dict(family='Calibri', size=16)
            ),
            tickvals=pd.date_range(
                str(df['Time'].iloc[0])[0:10],
                str(df['Time'].iloc[-1])[0:10],
                freq='5d'
            ),
            rangeselector=dict(
                x=0,
                y=1.05,
                buttons=list([
                    dict(count=7,
                        label='1w',
                        step='day',
                        stepmode='backward'),
                    dict(count=1,
                        label='1m',
                        step='month',
                        stepmode='backward'),
                    dict(count=6,
                        label='6m',
                        step='month',
                        stepmode='backward'),
                    dict(count=1,
                        label='1y',
                        step='year',
                        stepmode='backward'),
                    dict(step='all')
                ])
            ),
            showgrid=False
        ),
        yaxis=dict(
            title=dict(
                text='<b>Depth (m)</b>',
                font=dict(family='Calibri', size=16)
            ),
            autorange='reversed'),
        hovermode='closest'
    )

    fig = go.Figure(data=data,layout=layout)
    fig['layout']['xaxis'].update(ticktext=5*np.array(list(range(len(fig['layout']['xaxis']['tickvals'])))))
    return fig

#default wellbore
df_timevsdepth = data_extraction.get_timevsdepth('15_9_19_A')

#define time/depth curve page layout
page_layout = html.Div([
    html.H3(['Time/depth curve']),
    html.Div(id='dropdown-output', style={'paddingBottom': '10px', 'border-bottom': '1px solid black', 'font-weight': 'bold'}),
    html.Br(),
    html.Div(dcc.Graph(
        id='timevsdepth-plot',
        figure=timevsdepth_plot(df_timevsdepth),
        config=dict(displayModeBar=False)
    ), style={'display': 'block'}
)])

#callback to change the plot according to wellbore selection
@app.callback(
    Output('timevsdepth-plot', 'figure'),
    [Input('wells-dropdown', 'value')]
            )
def display_timevsdepth_plot(value):
    df_timevsdepth = data_extraction.get_timevsdepth(value)
    return timevsdepth_plot(df_timevsdepth)
