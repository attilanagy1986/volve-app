import dash


external_stylesheets = ['https://cdn.jsdelivr.net/gh/attilanagy1986/Dash-css@master/undo.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Volve app'
server = app.server
app.config.suppress_callback_exceptions = True
