import argparse
from os import environ
import yaml
import sys

# Read in argument(s)
description = 'Retrieve list of exclusions for specific job'
   
parser = argparse.ArgumentParser(     description=__doc__)
parser.add_argument('-c', '--CONFIG', nargs='?', type=str.lower, dest='CONFIG', help="Enter name of config file to search", required=True)
parser.add_argument('-e', '--EXCLUSIONS', nargs='?', type=str.upper, default="ALERT_EXCLUSIONS", dest='EXCLUSIONS', help="Enter name of parameter to retrieve")
parser.add_argument('-d', '--VALUE', nargs='?', type=str.upper, dest='VALUE', help="Enter name of parameter to retrieve")
parser.add_argument('-z', '--zzzzz', dest='ZZZZZ', action='store_true')
args = parser.parse_args()
config = args.CONFIG
param_value = args.VALUE
exclusions = args.EXCLUSIONS
z = args.ZZZZZ
#print("z:",z)


# Import Pipeline environment variables 
ids_job_name = environ.get('IDS_JOB_NAME')
print("ids_job_name", ids_job_name)
print("exclusions:", exclusions)
print("config:", config)

# read in config file
def read_config(config_file):
  with open(config, 'r') as f:
    try:
      pipeline_config = yaml.load(f)
    except yaml.YAMLError as exc:
      print(exc)
  return pipeline_config

def retrieve_config_value(config_file, param): 
  pipeline_config = read_config(config_file)
  stack = list(pipeline_config.items())
 # print("stack:", stack)
  visited = set() 
  while stack: 
    k, v = stack.pop() 
    if isinstance(v, dict):
      if param in [x for z in v for x in z if type(z)==list] or param in v:
        print(v[param])
      if k not in visited: 
        stack.extend(v.items()) 
      else: 
        print("%s: %s" % (k, v)) 
      visited.add(k)
 
def get_job_exclusions(config, exclusions, ids_job_name):    
    exclude = ""
    pipeline_config = read_config(config)
    for exc in pipeline_config[exclusions][ids_job_name]:      
        exclude += ";" + exc     
    return exclude
           

def main():
   # myprint(pipeline_config)
    if z:
    #    print("Main found alert exclusions")
    	print("config:", config)
    	print("exclusions:", exclusions)
    	print("ids_job_name:", ids_job_name)
        alerts = get_job_exclusions(config, exclusions, ids_job_name)
        print("alerts:", alerts)
 #       return alerts
    elif param_value:
        #config_value = get_config_value(pipeline_config, param_value)
        print(read_config(config))
    #   print(config_value)
    else:
        print("parameter not passed correctly")
    #print("alerts2:", alerts)
    #return alerts
if __name__ == '__main__':
    main()