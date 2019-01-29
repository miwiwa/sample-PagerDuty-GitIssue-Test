#!/usr/bin/env python

try:
    import argparse
    from os import environ
    import yaml
    import sys
    import pipeline
except ImportError as L_err:
    print("ImportError: {0}".format(L_err))
    raise L_err
    
    
# Read in argument(s)
description = 'Helper functions for Pipeline Config file'
   
parser = argparse.ArgumentParser(     description=__doc__)
parser.add_argument('-c', '--CONFIG', nargs='?', type=str.lower, dest='CONFIG', help="Enter name of config file to search")
parser.add_argument('-d', '--VALUE', nargs='?', type=str.upper, dest='VALUE', help="Enter name of parameter to retrieve")#parser.add_argument('-e', '--EXCLUSIONS_FLAG', dest='EXCLUSION_FLAG', action='store_true')
# Additional arguments from create_alert
parser.add_argument('-a', '--ALERTS', nargs='+', type=str.lower, dest='ALERTS', help="Enter 'incident', 'issue', and/or 'message' to send info to PagerDuty, Git, or Slack")#, required=True)
parser.add_argument('-s', '--STATUS', nargs='?', type=str.lower, dest='STATUS', default='Executed', help="Enter 'started' or 'completed' for Slack alerts")
parser.add_argument('-e', '--EXCLUSIONS_FLAG', dest='EXCLUSION_FLAG', action='store_true')

args = parser.parse_args()
config = args.CONFIG
param_value = args.VALUE
alert_check = args.EXCLUSION_FLAG

# Import Pipeline environment variables 
ids_job_name = environ.get('IDS_JOB_NAME')

# Reads in config file to dict
def read_config(config):
  with open(config, 'r') as f:
    print("reading yaml file")
    try:
      pipeline_config = yaml.load(f)
    except yaml.YAMLError as exc:
      print("Yaml file not formatted correctly")
      print("exc:", exc)
    except UnboundLocalError as exc:
      print("Yaml file not formatted correctly")
      print("exc:", exc)
    finally:
      return pipeline_config

# Return key value from pipeline.config
def retrieve_config_value(config_file, param): 
  pipeline_config = read_config(config_file)
  stack = list(pipeline_config.items())
  visited = set() 
  while stack: 
    k, v = stack.pop() 
    if isinstance(v, dict):
      if param in [x for alert_check in v for x in alert_check if type(alert_check)==list] or param in v: 
        print v[param]
        return v[param]
      if k not in visited: 
        stack.extend(v.items()) 
      else: 
        print("%s: %s" % (k, v)) 
      visited.add(k)
      
 # Return exclusions listed in pipeline.config as list
def get_job_exclusions(config, param_value, ids_job_name):      
    exclude = []
    pipeline_config = read_config(config)
    try:
        for exc in pipeline_config[param_value][ids_job_name]:
            print(exc)
    	    exclude.append(exc)
    except KeyError:
        return ids_job_name
    except TypeError:
        print("WARNING: Job listed in exclusions with no alerts to exclude. Sending all alerts")

    return exclude
           

def main():
    if alert_check:
        alerts = get_job_exclusions(config, param_value, ids_job_name)
        print(alerts)
        return alerts
    elif param_value:
        config_value = retrieve_config_value(config, param_value)
        print(config_value),
    else:
        print("parameter not passed correctly")

if __name__ == '__main__':
    main()