import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#import app and the separate app pages
from app import app
import volve_wells
import timevsdepth
import operations

#wellbore names for dropdown selection
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

#define the app layout
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

#callback to update page content
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def populate_content(url):
    if url == '/volve_wells':
        return volve_wells.page_layout
    elif url == '/timevsdepth':
        return timevsdepth.page_layout
    elif url == '/operations':
        return operations.page_layout

#callback for mulltipage persistence of the wellbore dropdown
@app.callback(
    Output('external-page-wells', 'style'),
    [Input('url', 'pathname')]
)
def hide_external(url):
    if url == '/volve_wells':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

#callback to display the selected wellbore name
@app.callback(
    Output('dropdown-output', 'children'),
    [Input('wells-dropdown', 'value')]
)
def display_dropdown_contents(val):
    if val:
        return f'Wellbore selected: {wells_dict[val]}'

#run the app
if __name__ == '__main__':
    app.run_server()
