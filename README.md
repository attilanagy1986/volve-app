Integrated web application for the OpenLab Drilling Simulator, the purpose is to create new configurations based on actual well data extracted from the Volve dataset (disclosed by Equinor). The app is created with Python using the Dash framework and Plotly library. The app is deployed at http://openlab.herokuapp.com. The OpenLab Drilling Simulator (developed by NORCE, formerly IRIS) can be accessed at https://live.openlab.app. No registration is needed, the simulator can be used by signing in with a Google account.

**Repository structure**\
Configurations folder:\
well configurations in .json (to create configurations in OpenLab)

Data folder:\
.csv files holding well data (to display well data in this app)

Python scripts:\
app.py initiates the Dash.app\
index.py defines the layout of the app\
openlab_app.py is a single bundle of all the scripts\
the other .py files define the layout and the content of the separate pages

requirements.txt:\
contains the Python dependencies

**Starting the app**\
Online:\
http://openlab.herokuapp.com \
Local:\
clone the repository, then run index.py to start the app\
alternatively run openlab_app.py, which contains all the scripts in a single bundle\
the app runs at http://127.0.0.1:8050 (local server)

**App structure**\
Wells page:\
General info about the 25 Volve wellbores, use the dropdown to select.

Hole section, Wellpath, Fluid, Drillstring, Geopressures, Geothermal pages:\
After the selection of a wellbore, the well configuration details are displayed by interactive graphs and tables. All graphs display information on hover, 3D well trajectories can also be rotated.

OpenLab page:\
Select a wellbore and a hole section, then provide the OpenLab credentials generated in the Settings of the OpenLab Web Client ('Generate Python login script'). Click the 'Create configuration' button, the selected wellbore configuration is sent directly to the OpenLab Web client. Ready to start a simulation in OpenLab.
