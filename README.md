# openlab-app

Integrated web application for the OpenLab Drilling Simulator to create new configurations based on actual well technical data extracted from the Volve dataset disclosed by Equinor.

The OpenLab Web Client can be accessed at https://live.openlab.app/. No registration is needed, the simulator can be used by signing in with a Google account.

This app is deployed to heroku at https://openlab.herokuapp.com/.
To start the app on a local server, download this repository and run 'index.py'. In most cases the local server is at http://127.0.0.1:8050/.

Wells page: general info about 25 Volve wellbores, use the dropdown to select.

Hole section, Wellpath, Fluid, Drillstring, Geopressures, Geothermal pages: after the selection of a wellbore, the well configuration details are displayed by the means of interactive graphs and tables. All graphs display information on hover, while the 3D well trajectories can also be rotated.

OpenLab page:
Select a wellbore and a hole section, then provide the OpenLab credentials generated in the Settings of the OpenLab Web Client. By clicking the 'Create configuration' button, the selected wellbore configuration is sent directly to the OpenLab Web client, and is ready to start simulations.
