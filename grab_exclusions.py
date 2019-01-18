import argparse
from os import environ
import yaml
import sys

# Read in argument(s)
description = 'Retrieve list of exclusions for specific job'
   
parser = argparse.ArgumentParser(     description=__doc__)
parser.add_argument('-c', '--CONFIG', nargs='?', type=str.lower, dest='CONFIG', help="Enter name of config file to search", required=True)
parser.add_argument('-e', '--EXCLUSIONS', nargs='?', type=str.upper, dest='EXCLUSIONS', help="Enter name of parameter to retrieve")
parser.add_argument('-d', '--VALUE', nargs='?', type=str.upper, dest='VALUE', help="Enter name of parameter to retrieve")
args = parser.parse_args()
config = args.CONFIG
param_value = args.VALUE
exclusions = args.EXCLUSIONS


# Import Pipeline environment variables 
ids_job_name = environ.get('IDS_JOB_NAME')

# read in config file
with open(config, 'r') as f:
    try:
        pipeline_config = yaml.load(f)
    except yaml.YAMLError as exc:
        print(exc)

values = pipeline_config.values() 
 
def get_job_exclusions():
    #print(pipeline_config[exclusions][ids_job_name])
    #for key in pipeline_config:
     #   if key in param_value:
      #      if "EXCLUSIONS" in param_value:
    exclude = ""
    for exc in pipeline_config[exclusions][ids_job_name]:
        print("exc", exc)
        exclude += ";" + exc
    return exclude
       # print("exclude:", exclude)
        #print("exclude", exc)
        #exclude = sys.stdout.write(';')
        #exclude += exc
    #return exclude
          #  else:
           #     print("Exclusions not in param_value")
            #    sys.stdout.write(pipeline_config.get(param_value, "Value doesn't exist"))
       # else:
           # print(param_value, "not found in", config)
        #    print("Key not in param_value")

#def get_config_value()
def get_config_value(data, target):
    for key, value in data['CD'].items():
    	#print("target:", target)
    	#print("key:", key)j
    	#print("value:", value)
        if isinstance(value, dict):
            print("value is dict")
            return get_config_value(value, target)
        elif key == target:
            print("key equals target")
            print("target", target)
            print("key", key)
            return value    

def main():
    print("Main exclusions:", exclusions)
    if "ALERT_EXCLUSIONS" in exclusions:
        print("Main found alert exclusions")
        get_job_exclusions()
    elif param_value:
        config_value = get_config_value(pipeline_config, param_value)
        print(config_value)
    else:
        print("parameter not passed correctly")
        
if __name__ == '__main__':
    main()