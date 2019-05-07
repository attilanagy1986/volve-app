import dash_table
import dash_html_components as html
import pandas as pd


df_wells = pd.read_csv('Data/volve_wells.csv', sep=';')

page_layout = html.Div([
    dash_table.DataTable(
        id='wells-table',
        columns=[{"name": i, "id": i} for i in df_wells.columns],
        data=df_wells.to_dict("rows"),
        style_header={'font-family': 'Calibri', 'font-weight': 'bold'},
        style_cell={'padding':'10px', 'font-family': 'Calibri', 'font-size': '16px', 'width': '100px'}
)], style={'width':'70%'})
