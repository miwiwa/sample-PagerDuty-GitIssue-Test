import argparse
from os import environ
import yaml
import sys

# Read in argument(s)
description = 'Retrieve list of exclusions for specific job'
   
parser = argparse.ArgumentParser(     description=__doc__)
parser.add_argument('-c', '--CONFIG', nargs='?', type=str.lower, dest='CONFIG', help="Enter name of config file to search", required=True)
parser.add_argument('-e', '--EXCLUSIONS', nargs='?', type=str.upper, dest='VALUE', help="Enter name of parameter to retrieve")
parser.add_argument('-d', '--VALUE', nargs='?', type=str.upper, dest='VALUE', help="Enter name of parameter to retrieve")
args = parser.parse_args()
config = args.CONFIG
param_value = args.VALUE
#exclusions - args.EXCLUSIONS


# Import Pipeline environment variables 
ids_job_name = environ.get('IDS_JOB_NAME')

# read in config file
with open(config, 'r') as f:
    try:
        pipeline_config = yaml.load(f)
    except yaml.YAMLError as exc:
        print(exc)


values = pipeline_config.values()
print(values)
 
 
#print("keys:",[k for k,v in pipeline_config.items()])
#print("values:",[v for k,v in pipeline_config.items()])
# output exclusions for specific job
#if param_value in pipeline_config.values():
#if param_value in pipeline_config:
for key in pipeline_config:
    if key in param_value:
        if "EXCLUSIONS" in param_value:
            for exc in pipeline_config[param_value][ids_job_name]:
                sys.stdout.write(';')
                sys.stdout.write(exc)
        else:
            print("Exclusions not in param_value")
            sys.stdout.write(pipeline_config.get(param_value, "Value doesn't exist"))
    else:
       # print(param_value, "not found in", config)
        print("Key not in param_value")

#def get_config_value()
def get_config_value(data, target):
    for key, value in data.items():
        if isinstance(value, dict):
            yield get_config_value(value, target)
        elif key == target:
            yield value    

def main():
    for x in find_by_key(config, param_value):
        print(x)
        
if __name__ == '__main__':
    main()