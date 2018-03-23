import dash
from dash.dependencies import Output, Event, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.plotly as py
import random
import plotly.graph_objs as go
from collections import deque
import csv
import datetime as dt
import dash_table_experiments as dt1
import pandas as pd

app_colors = {
    'background': '#0C0F0A',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
    }

X = deque(maxlen=20)
Xi =[]

Y0 = deque(maxlen=20)
Y0.append(0)
Yi0 =[]

Y1 = deque(maxlen=20)
Y1.append(0)
Yi1 =[]

Y2 = deque(maxlen=20)
Y2.append(0)
Yi2 =[]

Y3 = deque(maxlen=20)
Y3.append(0)
Yi3 =[]

Y4 = deque(maxlen=20)
Y4.append(0)
Yi4 =[]

keyword=[]
score=[]
emotion=[]
tweet=[]
count = 0

with open('output.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Xi.append(dt.datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S'))
        emotion.append(row['Emotion'])
        score.append(row['Score'])
        keyword.append(row['Keyword'])
        tweet.append(row['Tweet'])
        


app = dash.Dash(__name__)
app.layout = html.Div(
    [   html.Div(className='container-fluid', children=[html.H2('Twitter Emotion Analysis', style={'color':"#CECECE"}),
                                                        html.H5('Search:', style={'color':app_colors['text']}),
                                                  dcc.Input(id='sentiment_term', value=keyword[count], type='text', style={'color':app_colors['someothercolor']}),
                                                  ],
                 style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000}),
        
        html.Div(className='row', children=[html.Div(dcc.Graph(id='live-graph', animate=False), className='col s12 m6 l6')]),
        
        dcc.Interval(
            id='graph-update',
            interval=2*1000
        ),
            ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])

def update_graph_scatter():
    global count

    if emotion[count] == 'fear':
        Y0.append(Y0[-1]*0.8+float(score[count])*0.2)
        Y1.append(Y1[-1]-Y1[-1]*0.1)
        Y2.append(Y2[-1]-Y2[-1]*0.1)
        Y3.append(Y3[-1]-Y3[-1]*0.1)
        Y4.append(Y4[-1]-Y4[-1]*0.1)
    elif emotion[count] == 'disgust':
        Y1.append(Y1[-1]*0.8+float(score[count])*0.2)
        Y0.append(Y0[-1]-Y0[-1]*0.1)
        Y2.append(Y2[-1]-Y2[-1]*0.1)
        Y3.append(Y3[-1]-Y3[-1]*0.1)
        Y4.append(Y4[-1]-Y4[-1]*0.1)
    elif emotion[count] == 'sadness':
        Y2.append(Y2[-1]*0.8+float(score[count])*0.2)
        Y1.append(Y1[-1]-Y1[-1]*0.1)
        Y0.append(Y0[-1]-Y0[-1]*0.1)
        Y3.append(Y3[-1]-Y3[-1]*0.1)
        Y4.append(Y4[-1]-Y4[-1]*0.1)
    elif emotion[count] == 'joy':
        Y3.append(Y3[-1]*0.8+float(score[count])*0.2) 
        Y1.append(Y1[-1]-Y1[-1]*0.1)
        Y2.append(Y2[-1]-Y2[-1]*0.1)
        Y0.append(Y0[-1]-Y0[-1]*0.1)
        Y4.append(Y4[-1]-Y4[-1]*0.1)
    elif emotion[count] == 'anger':
        Y4.append(Y4[-1]*0.8+float(score[count])*0.2) 
        Y1.append(Y1[-1]-Y1[-1]*0.1)
        Y2.append(Y2[-1]-Y2[-1]*0.1)
        Y3.append(Y3[-1]-Y3[-1]*0.1)
        Y0.append(Y0[-1]-Y0[-1]*0.1)
    else:
        pass  

    X.append(Xi[count])
    
    count = count+1
    trace0 = go.Scatter(
            x=list(X),
            y=list(Y0),
            name='fear',
            mode= 'lines+markers'
            )
    
    trace1 = go.Scatter(
            x=list(X),
            y=list(Y1),
            name='disgust',
            mode= 'lines+markers'
            )
    trace2 = go.Scatter(
            x=list(X),
            y=list(Y2),
            name='sadness',
            mode= 'lines+markers'
            )
    trace3 = go.Scatter(
            x=list(X),
            y=list(Y3),
            name='joy',
            mode= 'lines+markers'
            )
    trace4 = go.Scatter(
            x=list(X),
            y=list(Y4),
            name='anger',
            mode= 'lines+markers'
            )
    
    data = [trace0, trace1, trace2, trace3, trace4]
    return {'data': data,'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis=dict(range=[min(min(Y0),min(Y1),min(Y2),min(Y3),min(Y4))-0.01,max(max(Y0), max(Y1), max(Y2), max(Y3), max(Y4))+0.01]))}



if __name__ == '__main__':
    app.run_server(debug=False)