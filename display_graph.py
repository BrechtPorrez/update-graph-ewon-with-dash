import mysql.connector
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


app = dash.Dash()

#create mySQL connection
try:
    con = mysql.connector.connect(
        host="*****",
        user="*****",
        passwd="*****",
        database="*****",
    )
    print ('connected:',con)
except Exception as e:
    print(e)

# read Id and name of EWon's
db_ewon = con.cursor()
db_ewon.execute("SELECT Id,name FROM esync_stations")
installations = db_ewon.fetchall()
installations_dict = {}
total_dict = {}


for item in installations:
    # item[0]: installationID
    # item[1]: name installation

    # first we read all the parameters of the current installationID
    parameters_dict = {}
    db_parameters = con.cursor()
    db_parameters.execute("SELECT Id,name FROM esync_tags WHERE stationID=%i" % item[0])
    parameters = db_parameters.fetchall()
    parameters_dict = {}

    # now we write all the the parameters of all to installations to a dict, this is not the actual data, these are only
    # the values displayed in the dropdown menus
    # this works more efficient during runtime and the parameters are almost never updated, only the data in the
    # parameters is updated a lot
    for par in parameters:
        parameters_dict[par[0]] = par[1]
    total_dict[item[0]] = parameters_dict
    installations_dict[item[0]] = item[1]

# create layout
app.layout = html.Div(children=[
    html.Div(children='Maximum value Y-axis:'),
    dcc.Input(id='max_value', value='100', type='text'),
    html.Div(children='Select installation:'),
    dcc.Dropdown(
        id='dropdown-machine',
        options=[{'label': machine, 'value': machineID} for machineID, machine in installations_dict.items()],
        value=10
    ),
    dcc.Dropdown(
        id='dropdown-tag',
        value=693
    ),
    html.Div(id='output-graph'),
])


# update dropdown tags
@app.callback(
    Output(component_id='dropdown-tag', component_property='options'),
    [Input(component_id='dropdown-machine', component_property='value')]
)
def updateDropdown(input_data):
    return [{'label': tag, 'value': tagID} for tagID, tag in total_dict[input_data].items()]


# update graph
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='dropdown-tag', component_property='value'),
     Input(component_id='max_value', component_property='value')]
)
def updateGraph(input_data, maxY):
    df = pd.read_sql_query('SELECT _date,Val FROM esync_tagshistory WHERE TagId=%i AND DATE(_date)>"2015-01-01"' % (int(input_data)), con)
    return dcc.Graph(
        id='example-graph2',
        figure={
            'data': [
                {'x': df._date, 'y': df.Val, 'type': 'line', 'name': input_data},
            ],
            'layout': go.Layout(yaxis=dict(range=[0, int(maxY)], titlefont=dict(color='#1f77b4'), tickfont=dict(color='#1f77b4'),),
                                title=input_data)
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)

