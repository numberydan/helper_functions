import os
import pandas as pd
import numpy as np
import copy
from math import log
import datetime
from pandas.tseries.offsets import *
import time
import matplotlib
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
init_notebook_mode()
import plotly.graph_objs as go
from plotly.tools import FigureFactory as ff
from plotly import tools


def to_unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt-epoch).total_seconds()*1000
            
def plotly_pandas_hack(data,title,x_axis_name,y_axis_name):
    starting_dictionary = {'data': [],
    'layout': {'title':title,
    'xaxis':  {'title':x_axis_name,'range': [to_unix_time(data.index.min()), to_unix_time(data.index.max()+MonthBegin(2))]},
    'yaxis':  {'title':y_axis_name},
              }}
    for columns in data.columns.tolist():
        current = {
            'mode': 'lines',
            'name': columns,
            'type': 'scatter',
            'x': data.index,
            'y': data[columns].values.tolist()
        }
        starting_dictionary["data"].append(current)
    iplot(starting_dictionary)

def plotly_pandas_hack_markers(data,title,x_axis_name,y_axis_name):
    starting_dictionary = {'data': [],
    'layout': {'title':title,
    'xaxis':  {'title':x_axis_name,'range': [to_unix_time(data.index.min()), to_unix_time(data.index.max()+MonthBegin(2))]},
    'yaxis':  {'title':y_axis_name},
              }}
    for columns in data.columns.tolist():
        current = {
            'mode': 'lines+markers',
            'name': columns,
            'type': 'scatter',
            'x': data.index,
            'y': data[columns].values.tolist()
        }
        starting_dictionary["data"].append(current)
    iplot(starting_dictionary)    
    
def plotly_pandas_hack_markers_log(data,title,x_axis_name,y_axis_name):
    starting_dictionary = {'data': [],
    'layout': {'title':title,
    'xaxis':  {'title':x_axis_name,'range': [to_unix_time(data.index.min()), to_unix_time(data.index.max()+MonthBegin(2))]},
    'yaxis':  {'title':y_axis_name, 'type':'log'},
              }}
    for columns in data.columns.tolist():
        current = {
            'mode': 'lines+markers',
            'name': columns,
            'type': 'scatter',
            'x': data.index,
            'y': data[columns].values.tolist()
        }
        starting_dictionary["data"].append(current)
    iplot(starting_dictionary)        

