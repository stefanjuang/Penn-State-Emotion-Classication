import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.plotly as py
import random
import plotly.graph_objs as go
from collections import deque
import csv
import datetime as dt

X = deque(maxlen=20)
Xi =[]

Y0 = deque(maxlen=20)
Yi0 =[]

Y1 = deque(maxlen=20)
Yi1 =[]

Y2 = deque(maxlen=20)
Yi2 =[]

Y3 = deque(maxlen=20)
Yi3 =[]

count = 0

with open('sample2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Xi.append(dt.datetime.strptime(row['Timestamp'], '%m/%d/%Y %H:%M'))
        Yi0.append(row['happy'])
        Yi1.append(row['sadness'])
        Yi2.append(row['surprise'])
        Yi3.append(row['anger'])
        
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=False),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    global count
    X.append(Xi[count])
    print(X)
    Y0.append(float(Yi0[count]))
    Y1.append(float(Yi1[count]))
    Y2.append(float(Yi2[count]))
    Y3.append(float(Yi3[count]))
    count = count+1
    trace0 = go.Scatter(
            x=list(X),
            y=list(Y0),
            name='happy',
            mode= 'lines+markers'
            )
    
    trace1 = go.Scatter(
            x=list(X),
            y=list(Y1),
            name='sadness',
            mode= 'lines+markers'
            )
    trace2 = go.Scatter(
            x=list(X),
            y=list(Y2),
            name='surprise',
            mode= 'lines+markers'
            )
    trace3 = go.Scatter(
            x=list(X),
            y=list(Y3),
            name='anger',
            mode= 'lines+markers'
            )
    
    data = [trace0, trace1, trace2, trace3]
    return {'data': data,'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis=dict(range=[min(Y1),max(Y0)]))}



if __name__ == '__main__':
    app.run_server(debug=False)