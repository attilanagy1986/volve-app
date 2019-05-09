import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

from app import app
import data_extraction

#function to create the operations timeline plot
def operations_plot(df):

    data = [
        dict(
            Task='<b>Activities</b>',
            Start=df['Start'].loc[num],
            Finish=df['End'].loc[num],
            Resource=df['State'].loc[num].replace(' ','_')
            )
        for num in df.index
        ]

    colors = dict(
        equipment_failure='rgb(0,115,172)',
        injury='rgb(255,210,0)',
        mud_loss='rgb(183,18,124)',
        circulation_loss='rgb(183,18,124)',
        stuck_equipment='rgb(149,99,47)',
        success='rgb(7,178,178)',
        operation_failed='rgb(204,19,51)'
    )

    fig = ff.create_gantt(
                        data,
                        title=None,
                        colors=colors,
                        show_colorbar=True,
                        index_col='Resource',
                        bar_width=1,
                        group_tasks=True
                        )

    text = [
        "<b>Start:</b> {}<br>"
        "<b>End:</b> {}<br>"
        "<b>Duration:</b> {}<br>"
        "<b>MD:</b> {} m<br>"
        "<b>Operation:</b> {}<br>"
        "<b>State:</b> {}<br>"
        "<b>Comment:</b> {}"
        .format(
                str(df['Start'].loc[i])[:16],
                str(df['End'].loc[i])[:16],
                str(df['Duration'].loc[i])[7:12],
                df['MD (m)'].loc[i],
                df['Operation'].loc[i],
                df['State'].loc[i],
                df['Comment'].loc[i].replace('.','<br>')
                )
        for i in df.index
        ]

    for i in range(len(text)):
        fig['data'][i].update(text=text[i], hoverinfo='text')

    for i in range(len(fig['layout']['shapes'])):
        fig['layout']['shapes'][i].update(line={'width':0.1, 'color':'rgb(255,255,255)'})

    fig['layout']['xaxis']['rangeselector'].update(
        x=0,
        y=1.5,
        buttons=[
            dict(count=1,
                label='1d',
                step='day',
                stepmode='backward'),
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

    fig['layout'].update(
                        autosize=False,
                        width=1400,
                        height=240,
                        margin=dict(r=0),
                        legend=dict(
                            orientation='h',
                            x=0,
                            y=-1.2
                        ),
                        hovermode='closest')

    fig['layout']['xaxis'].update(title=dict(text='<b>Days</b>', font=dict(size=12)),tickvals=pd.date_range(str(df['Start'].iloc[0])[0:10], str(df['End'].iloc[-1])[0:10], freq='5d'))
    fig['layout']['xaxis'].update(ticktext=5*np.array(list(range(len(fig['layout']['xaxis']['tickvals'])))))

    return fig

#default wellbore
df_operations = data_extraction.get_operations('15_9_19_A')

#define page layout
page_layout = html.Div([
    html.H3(['Operations']),
    html.Div(id='dropdown-output', style={'paddingBottom': '10px', 'border-bottom': '1px solid black', 'font-weight': 'bold'}),
    html.Br(),
    html.Div(dcc.Graph(
        id='operations-plot',
        figure=operations_plot(df_operations),
        config=dict(displayModeBar=False)
    ), style={'display': 'block'}
)])

#callback to change the plot according to wellbore selection
@app.callback(
    Output('operations-plot', 'figure'),
    [Input('wells-dropdown', 'value')]
    )
def display_operations_plot(value):
    df_operations = data_extraction.get_operations(value)
    return operations_plot(df_operations)
