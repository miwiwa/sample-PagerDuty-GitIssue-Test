import argparse
from os import environ
import yaml
import sys

# Read in argument(s)
description = 'Retrieve list of exclusions for specific job'
   
parser = argparse.ArgumentParser(     description=__doc__)
parser.add_argument('-c', '--CONFIG', nargs='?', type=str.lower, dest='CONFIG', help="Enter name of config file to search", required=True)
parser.add_argument('-d', '--value', nargs='?', type=str.upper, dest='VALUE', help="Enter name of parameter to retrieve")
args = parser.parse_args()
config = args.CONFIG
param_value = args.VALUE
print("param_value:", param_value)

# Import Pipeline environment variables 
ids_job_name = environ.get('IDS_JOB_NAME')

# read in config file
with open(config, 'r') as f:
    try:
        pipeline_config = yaml.load(f)
    except yaml.YAMLError as exc:
        print(exc)
print("Type:",type(pipeline_config))

x = isinstance(pipeline_config, dict)
print("x",x)
print(pipeline_config)

values = pipeline_config.values()
print(values)
 
if param_value in pipeline_config:
  print "blah"
else:
  print "boo" 
# output exclusions for specific job
#if param_value in pipeline_config.values():
#if param_value in pipeline_config:
for key in pipeline_config:
    if key in param_value:
        if key in "EXCLUSIONS"
            for exc in pipeline_config[param_value][ids_job_name]:
                sys.stdout.write(';')
                sys.stdout.write(exc)
        else:
        sys.stdout.write(pipeline_config.get(param_value, "Value doesn't exist"]))
    else:
        print(param_value, "not found in", config)
        exit()
    

