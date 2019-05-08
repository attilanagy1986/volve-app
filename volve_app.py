import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import plotly.graph_objs as go
import os
import xml.etree.ElementTree as et
import pandas as pd
import numpy as np
from datetime import datetime


external_stylesheets = ['https://cdn.jsdelivr.net/gh/attilanagy1986/Dash-css@master/undo.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Volve app'
server = app.server
app.config.suppress_callback_exceptions = True


def get_timevsdepth(well):

    report_list = os.listdir('Reports')

    time = []
    md = []
    section = []
    summary = []

    df = pd.DataFrame(
        list(zip(
            time,
            md,
            section,
            summary
        )),
        columns = [
            'Time',
            'MD (m)',
            'Section (in)',
            'Summary'
    ])

    os.chdir('Reports')

    for file in report_list:
        if file[:-15] == well:
            report_tree = et.parse(file)
            report_root = report_tree.getroot()

            time = []
            md = []
            section = []
            summary = []
            time_temp = True
            md_temp = True
            section_temp = True
            summary_temp = True

            for child in report_root:
                for elem in child:
                    if elem.tag == '{http://www.witsml.org/schemas/1series}statusInfo':
                        for subelem in elem:
                            if subelem.tag == '{http://www.witsml.org/schemas/1series}dTim':
                                time.append(datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M'))
                                time_temp = False
                            elif subelem.tag == '{http://www.witsml.org/schemas/1series}md':
                                md.append(float(subelem.text) if float(subelem.text)>0 else 0)
                                md_temp = False
                            elif subelem.tag == '{http://www.witsml.org/schemas/1series}diaHole':
                                section.append(float(subelem.text))
                                section_temp = False
                            elif subelem.tag == '{http://www.witsml.org/schemas/1series}sum24Hr':
                                summary.append(subelem.text)
                                summary_temp = False
                            else:
                                pass

            if time_temp:
                time.append('None')
            if md_temp:
                md.append(0)
            if section_temp:
                section.append('-')
            if summary_temp:
                summary.append('-')

            df = df.append(
                pd.DataFrame(
                    list(zip(
                        time,
                        md,
                        section,
                        summary
                    )),
                    columns = [
                        'Time',
                        'MD (m)',
                        'Section (in)',
                        'Summary'
                    ]),
                ignore_index = True,
                sort = False
            )

    df.sort_values(['Time'], inplace=True)
    os.chdir('../')
    return df


def get_operations(well):

    report_list = os.listdir('Reports')

    start = []
    end = []
    md = []
    operation = []
    comment = []
    duration = []
    state = []

    df = pd.DataFrame(
        list(zip(
            start,
            end,
            md,
            duration,
            operation,
            comment,
            state
        )),
        columns = [
            'Start',
            'End',
            'MD (m)',
            'Duration',
            'Operation',
            'Comment',
            'State'
    ])

    os.chdir('Reports')

    for file in report_list:
        if file[:-15] == well:
            report_tree = et.parse(file)
            report_root = report_tree.getroot()

            start = []
            end = []
            md = []
            operation = []
            comment = []
            duration = []
            state = []

            for child in report_root:
                for elem in child:
                    if elem.tag == '{http://www.witsml.org/schemas/1series}activity':
                        for subelem in elem:
                            if 'dTimStart' in subelem.tag:
                                start.append(datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M'))
                                start_temp = datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M')
                            elif 'dTimEnd' in subelem.tag:
                                end.append(datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M'))
                                end_temp = datetime.strptime(subelem.text[:16], '%Y-%m-%dT%H:%M')
                            elif 'md' in subelem.tag:
                                md.append(subelem.text)
                            elif 'proprietaryCode' in subelem.tag:
                                operation.append(subelem.text)
                            elif 'comments' in subelem.tag:
                                comment.append(subelem.text)
                            elif 'stateDetailActivity' in subelem.tag:
                                state.append(subelem.text)
                            else:
                                pass
                        duration.append((end_temp-start_temp))

            df = df.append(
                pd.DataFrame(
                    list(zip(
                        start,
                        end,
                        md,
                        duration,
                        operation,
                        comment,
                        state
                    )),
                    columns = [
                        'Start',
                        'End',
                        'MD (m)',
                        'Duration',
                        'Operation',
                        'Comment',
                        'State'
                    ]),
                ignore_index = True,
                sort = False
            )

    df.sort_values(['Start'], inplace=True)
    os.chdir('../')
    return df


wells_dict = {
            '15_9_19_A': '15/9-19 A',
            '15_9_19_B': '15/9-19 B',
            '15_9_19_BT2': '15/9-19 BT2',
            '15_9_19_S': '15/9-19 S',
            '15_9_19_ST2': '15/9-19 ST2',
            '15_9_F_1': '15/9-F-1',
            '15_9_F_1_A': '15/9-F-1 A',
            '15_9_F_1_B': '15/9-F-1 B',
            '15_9_F_1_C': '15/9-F-1 C',
            '15_9_F_4': '15/9-F-4',
            '15_9_F_5': '15/9-F-5',
            '15_9_F_7': '15/9-F-7',
            '15_9_F_9': '15/9-F-9',
            '15_9_F_9_A': '15/9-F-9 A',
            '15_9_F_10': '15/9-F-10',
            '15_9_F_11': '15/9-F-11',
            '15_9_F_11_A': '15/9-F11 A',
            '15_9_F_11_B': '15/9-F-11 B',
            '15_9_F_11_T2': '15/9-F-11 T2',
            '15_9_F_12': '15/9-F-12',
            '15_9_F_14': '15/9-F-14',
            '15_9_F_15': '15/9-F-15',
            '15_9_F_15_A': '15/9-F-15 A',
            '15_9_F_15_B': '15/9-F-15 B',
            '15_9_F_15_C': '15/9-F-15 C',
            '15_9_F_15_D': '15/9-F-15 D'
            }

app.layout = html.Div([
    dcc.Location(id='url'),
    dcc.Link(
            'Volve wells',
            href='/volve_wells',
            style={
                'color': 'rgb(0,0,0)',
                'font-size': '17px',
                'font-weight': 'bold'
                }),
    dcc.Link(
            'Time/depth curve',
            href='/timevsdepth',
            style={
                'color': 'rgb(0,0,0)',
                'font-size': '17px',
                'font-weight': 'bold',
                'paddingLeft':'25px'
                }),
    dcc.Link(
            'Operations',
            href='/operations',
            style={
                'color': 'rgb(0,0,0)',
                'font-size': '17px',
                'font-weight': 'bold',
                'paddingLeft':'25px'
                }),
    html.Div([
        html.H3(['Select a wellbore'], style={'paddingBottom': '10px', 'font-weight': 'bold', 'border-bottom': '1px solid black'}),
        dcc.Dropdown(
            options=[{'label':value, 'value':key} for key, value in wells_dict.items()],
            value='15_9_19_A',
            placeholder='Select a wellbore',
            id='wells-dropdown',
            style={'width':'50%'}
        ),
        html.Br(),
    ], id='external-page-wells', style={'paddingLeft':'25px'}),
    html.Div(id='page-content')
], style={'font-family': 'Calibri', 'paddingLeft':'25px', 'paddingRight':'25px'})

df_wells = pd.read_csv('Data/volve_wells.csv', sep=';')

volve_wells_layout = html.Div([
    dash_table.DataTable(
        id='wells-table',
        columns=[{"name": i, "id": i} for i in df_wells.columns],
        data=df_wells.to_dict("rows"),
        style_header={'font-family': 'Calibri', 'font-weight': 'bold'},
        style_cell={'padding':'10px', 'font-family': 'Calibri', 'font-size': '16px', 'width': '100px'}
)], style={'width':'70%'})


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


df_timevsdepth = get_timevsdepth('15_9_19_A')

timevsdepth_layout = html.Div([
    html.H3(['Time/depth curve']),
    html.Div(id='dropdown-output', style={'paddingBottom': '10px', 'border-bottom': '1px solid black', 'font-weight': 'bold'}),
    html.Br(),
    html.Div(dcc.Graph(
        id='timevsdepth-plot',
        figure=timevsdepth_plot(df_timevsdepth),
        config=dict(displayModeBar=False)
    ), style={'display': 'block'}
)])


@app.callback(
    Output('timevsdepth-plot', 'figure'),
    [Input('wells-dropdown', 'value')]
            )
def display_timevsdepth_plot(value):
    df_timevsdepth = get_timevsdepth(value)
    return timevsdepth_plot(df_timevsdepth)


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

df_operations = get_operations('15_9_19_A')

operations_layout = html.Div([
    html.H3(['Operations']),
    html.Div(id='dropdown-output', style={'paddingBottom': '10px', 'border-bottom': '1px solid black', 'font-weight': 'bold'}),
    html.Br(),
    html.Div(dcc.Graph(
        id='operations-plot',
        figure=operations_plot(df_operations),
        config=dict(displayModeBar=False)
    ), style={'display': 'block'}
)])


@app.callback(
    Output('operations-plot', 'figure'),
    [Input('wells-dropdown', 'value')]
    )
def display_operations_plot(value):
    df_operations = get_operations(value)
    return operations_plot(df_operations)



@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def populate_content(url):
    if url == '/volve_wells':
        return volve_wells_layout
    elif url == '/timevsdepth':
        return timevsdepth_layout
    elif url == '/operations':
        return operations_layout


@app.callback(
    Output('external-page-wells', 'style'),
    [Input('url', 'pathname')]
)
def hide_external(url):
    if url == '/volve_wells':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('dropdown-output', 'children'),
    [Input('wells-dropdown', 'value')]
)
def display_dropdown_contents(val):
    if val:
        return f'Wellbore selected: {wells_dict[val]}'


if __name__ == '__main__':
    app.run_server()
