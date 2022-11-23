import subprocess
import argparse
import time
import pandas as pd
import io 

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
    parser.add_argument('--gpu_user', help='username', default='aaa' )
    parser.add_argument('--gpu_address', help="ip", default="bbb")
    parser.add_argument('--by', help="by s", default=1)
    
    return parser.parse_args()

class GPU(): 
    def __init__(self):
        exit(1)

if __name__=='__main__':   
    args = parse_args()
    format = '--format=csv'
    query  = '--query-gpu='
    obs = ["timestamp","name","pci.bus_id","driver_version","pstate","pcie.link.gen.max",
            "pcie.link.gen.current","temperature.gpu","utilization.gpu","utilization.memory",
            "memory.total","memory.free","memory.used"]
    query = query+','.join(obs)

    command = get_command(gpu_user=args.gpu_user, gpu_address=args.gpu_address, command=['nvidia-smi',query,format])
    header = None 
    while True: 
        out = execute_command(command=command)
        data = pd.read_csv(io.StringIO(out), sep=",")
        print(data)
        time.sleep(int(args.by))

