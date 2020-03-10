import pandas as pd
import datetime
from pandas.tseries.offsets import *
import time
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
# to do, make flexible for dates vs categorical

dan_colorway = ["#2965CC", "#D13913", "#29A634", "#D99E0B", "#8F398F", "#00B3A4", "#DB2C6F", "#9BBF30", "#96622D", "#7157D9"]

def plotly_pandas(data,title='Title'
                       ,x_axis_name='X Axis',y_axis_name='Y Axis'
                      ,show_max_date=True,mode='lines'):
    starting_dictionary = {'data': [],
    'layout': {
        'title':title
        ,'legend':{'orientation':'h','xanchor':'center','y':1.1,'x':0.5}
        ,'xaxis':  {'title':x_axis_name
                    , 'showline':True
                    , 'linewidth':1
                    , 'linecolor':'#738694'
                    , 'mirror':True
                    , 'gridcolor':'#D8E1E8'
                    ,'range': [to_unix_time(data.index.min())
                              , to_unix_time(data.index.max()+MonthBegin(2))]
                  }
        ,'yaxis':  {'title':y_axis_name
                    , 'showline':True
                    , 'linewidth':1
                    , 'linecolor':'#738694'
                    , 'mirror':True
                    , 'gridcolor':'#D8E1E8'
                }
        ,'paper_bgcolor':'#FFFFFF'
        ,'plot_bgcolor':'#FFFFFF'
        ,'colorway':dan_colorway
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
