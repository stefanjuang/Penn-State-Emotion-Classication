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

app_colors = {
    'background': '#0C0F0A',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
    }

X = deque(maxlen=20)
X1 = deque(maxlen=20)
Xi =[]

Y0 = deque(maxlen=20)
Y0.append(0)

Y1 = deque(maxlen=20)
Y1.append(0)

Y2 = deque(maxlen=20)
Y2.append(0)

Y3 = deque(maxlen=20)
Y3.append(0)

Y4 = deque(maxlen=20)
Y4.append(0)

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
        html.Div(className='row', children=[html.Div(dcc.Graph(id='live-table', animate=False), className='col s12 m6 l6')]),
        
        html.Div(className='row', children=[html.Div(dcc.Graph(id='live-graph', animate=False), className='col s12 m6 l6'),
                                                html.Div(dcc.Graph(id='live-donut', animate=False), className='col s12 m6 l6')]),
        
        dcc.Interval(
            id='graph-update',
            interval=1.5*1000
        ),
        dcc.Interval(
            id='table-update',
            interval=1*1000
        ),
        dcc.Interval(
            id='donut-update',
            interval=1.5*1000
        ),
            ], style={'backgroundColor': app_colors['background'], 'height':'2000px',},
)


@app.callback(Output('live-table', 'figure'),
              events=[Event('table-update', 'interval')])
def update_table():
    trace = go.Table(
    header=dict(values=['Time', 'Tweets']),
    cells=dict(values=[Xi,tweet]))
    data1 = [trace] 
    return{'data':data1}

 
@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])

def update_graph_scatter():
    global count, Y0,Y1,Y2,Y3,Y4
    X.append(Xi[count])
    
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
    if emotion[count] == 'fear':
        Y0.append(Y0[-1]*0.95+float(score[count])*0.05)
        Y1.append(Y1[-1]*0.95)
        Y2.append(Y2[-1]*0.95)
        Y3.append(Y3[-1]*0.95)
        Y4.append(Y4[-1]*0.95)
    elif emotion[count] == 'disgust':
        Y1.append(Y1[-1]*0.95+float(score[count])*0.05)
        Y0.append(Y0[-1]*0.95)
        Y2.append(Y2[-1]*0.95)
        Y3.append(Y3[-1]*0.95)
        Y4.append(Y4[-1]*0.95)
    elif emotion[count] == 'sadness':
        Y2.append(Y2[-1]*0.95+float(score[count])*0.05)
        Y1.append(Y1[-1]*0.95)
        Y0.append(Y0[-1]*0.95)
        Y3.append(Y3[-1]*0.95)
        Y4.append(Y4[-1]*0.95)
    elif emotion[count] == 'joy':
        Y3.append(Y3[-1]*0.95+float(score[count])*0.05) 
        Y1.append(Y1[-1]*0.95)
        Y2.append(Y2[-1]*0.95)
        Y0.append(Y0[-1]*0.95)
        Y4.append(Y4[-1]*0.95)
    elif emotion[count] == 'anger':
        Y4.append(Y4[-1]*0.95+float(score[count])*0.05) 
        Y1.append(Y1[-1]*0.95)
        Y2.append(Y2[-1]*0.95)
        Y3.append(Y3[-1]*0.95)
        Y0.append(Y0[-1]*0.95)
    else:
        pass  

    count = count+1
    
    data = [trace0, trace1, trace2, trace3, trace4]
    return {'data': data,'layout' : go.Layout(title='Emotion Analysis for "{}" on Twitter'.format(keyword[count]),xaxis=dict(range=[min(X),max(X)]),yaxis=dict(range=[min(min(Y0),min(Y1),min(Y2),min(Y3),min(Y4))-0.01,max(max(Y0), max(Y1), max(Y2), max(Y3), max(Y4))+0.01]))}

@app.callback(Output('live-donut', 'figure'),
              events=[Event('donut-update', 'interval')])
def update_donut():
    labels = ['fear','disgust','sadness','joy','anger']
    values = [abs(Y0[-2]),abs(Y1[-2]),abs(Y2[-2]),abs(Y3[-2]),abs(Y4[-2])]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    tracepie = go.Pie(labels=labels, values=values,marker=dict(colors=colors, 
                           line=dict(color='#000000', width=2)))
    data2 = [tracepie] 
    return{'data':data2}

if __name__ == '__main__':
    app.run_server(debug=False)