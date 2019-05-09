Browser-based application for well data management and visualization. Data source is the daily drilling reports of the Volve Dataset (disclosed by Equinor). More info on the Dataset at https://data.equinor.com/authenticate. The app uses automated data extraction from the drilling reports, then displays information by interactive plots.

**Repository structure**\
Data folder:\
.csv file holding general well data on the Volve wellbores

Reports folder:\
daily drilling reports in .xml format

Python scripts:\
app.py initiates the Dash.app\
data_extraction.py holds scripts for automated parsing and data extraction
index.py defines the layout of the app\
volve_app.py is a single bundle of all the scripts\
the other .py files define the layout and the content of the separate pages

requirements.txt:\
contains the Python dependencies

**Starting the app**\
Online:\
http://volve.herokuapp.com \
Local:\
clone the repository, then run index.py to start the app\
alternatively run volve_app.py, which contains all the scripts in a single bundle\
the app runs at http://127.0.0.1:8050 (local server)

**App structure**\
Volve wells page:\
General info about the 25 Volve wellbores, use the dropdown to select.

Time/depth curve page:\
Displays an interactive time vs. depth curve. Hoverinfo consists of information on date, measured depth, section drilled and 24h summary. Zoom-in by drag-and-drop, zoom-out by double click. Range selector on the top left corner of the plot to specify the time range. The timeline (x-axis) functions as a range slider.

Operations page:\
Displays an interactive timeline of the operational activities. Hoverinfo consists of information on start and end time, duration, measured depth, operation phase, state of activity and comment. Each activity is colored according to the state of that certain activity. The following categories apply: equipment failure, injury, mud and circulation loss, operation failed, stuck equipment, success. Therefore drilling problems, as well as practices to solve the problem/mitigate the consequencies can be examined. Zoom-in by drag-and-drop, zoom-out by double click. Range selector on the top left corner of the plot to specify the time range. The timeline (x-axis) functions as a range slider.
