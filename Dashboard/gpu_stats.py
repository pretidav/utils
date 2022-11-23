import subprocess
import argparse
import time
import pandas as pd
import io 
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
import dash_daq as daq

def get_command(gpu_user,gpu_address,command=['nvidia-smi']): 
    full_address = '@'.join([gpu_user,gpu_address])
    prefix = ["ssh",full_address]
    for c in command: 
        prefix.append(c)
    return prefix

def execute_command(command): 
    #print('executing:\n{}'.format(' '.join(command)))
    out = subprocess.run(command, capture_output=True, text=True)
    return out.stdout

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_user', help='username', default='iride' )
    parser.add_argument('--gpu_address', help="ip", default="10.121.193.137")
    parser.add_argument('--by', help="by s", default=1)
    
    return parser.parse_args()

if __name__=='__main__':   
    args = parse_args()
    format = '--format=csv'
    query  = '--query-gpu='
    obs = ["timestamp","name","pci.bus_id","driver_version","pstate","pcie.link.gen.max",
            "pcie.link.gen.current","temperature.gpu","utilization.gpu","utilization.memory",
            "memory.total","memory.free","memory.used"]
    query = query+','.join(obs)

    command = get_command(gpu_user=args.gpu_user, gpu_address=args.gpu_address, command=['nvidia-smi',query,format])
    

    app = Dash(__name__)
    # app.layout = html.Div([
    #     dcc.Interval(
    #         id='interval-component',
    #         interval=1*1000
    #     ),
    #     daq.Gauge(
    #     id='my-gauge-1',
    #     label="Default",
    #     value=20,
    #     max=100,
    #     min=0,
    # )])
  

    header = None 
    while True: 
        out = execute_command(command=command)
        data = pd.read_csv(io.StringIO(out), sep=",")
        # print(data.columns)
        # print(int(data[' utilization.gpu [%]'].values[0].split('%')[0]))
        app.layout = html.Div([
            dcc.Interval(
            id='interval-component',
            interval=1*1000
        ),
            daq.Gauge(
                id='my-gauge-1',
                label="Default",
                value=0,
                max=100,
                min=0,
            )])
            
        @app.callback(Output('my-gauge-1', 'value'),
                Input('interval-component', 'interval'))
        def update_graph_scatter(interval):
            return int(data[' utilization.gpu [%]'].values[0].split('%')[0])
            
        app.run_server(debug=True)
        time.sleep(int(args.by))

