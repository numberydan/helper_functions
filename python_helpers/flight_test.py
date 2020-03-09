#obvi i copied this from a common set of things, i should not be importing all these things, clean this up
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

# to do, bring back abilty to set y range
# to do, bring back split axis ability
# to do, bring back scaling
# to do, add latest date
# to do, make flexible for dates vs categorical
def plotly_pandas(data,title='Title'
                       ,x_axis_name='X Axis',y_axis_name='Y Axis'
                      ,show_max_date=True,mode='lines'):
    starting_dictionary = {'data': [],
    'layout': {
        'title':title
        ,'legend':{'orientation':'h','xanchor':'center','y':1.1,'x':0.5}
        ,'xaxis':  {'title':x_axis_name
                   ,'range': [to_unix_time(data.index.min())
                              , to_unix_time(data.index.max()+MonthBegin(2))]
                  }
        ,'yaxis':  {'title':y_axis_name},
                  }
                          }
    
    
    if show_max_date:
        starting_dictionary['layout']['annotations'] = \
            [
                {
                    'text':'Max Date: ' + str(data.index.max())[:10]
                    ,'xref':'paper'
                    ,'yref':'paper'
                    ,'xanchor':'left'
                    ,'x':-0.05
                    ,'y':-0.15
                    ,'showarrow':False
                    ,'font':{'color':'#5C7080'}
                }
            ]
    
    for columns in data.columns.tolist():
        current = {
            'mode': mode,
            'name': columns,
            'type': 'scatter',
            'x': data.index,
            'y': data[columns].values.tolist()
        }
        starting_dictionary["data"].append(current)
        
    iplot(starting_dictionary)