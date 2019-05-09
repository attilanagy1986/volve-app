import dash

#external stylesheet for css styling
external_stylesheets = ['https://cdn.jsdelivr.net/gh/attilanagy1986/Dash-css@master/undo.css']

#initiating Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#title of the app
app.title = 'Volve app'
#initiate server
server = app.server
#if set to False, Dash will raise an exception due to the multipage structure of the app
app.config.suppress_callback_exceptions = True
