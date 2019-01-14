import argparse

# Read in argument(s)
description = 'Specify creation of incident/issue in Pagerduty and Git Issues'
   
parser = argparse.ArgumentParser(     description=__doc__)
parser.add_argument('-c', '--CONFIG', nargs='?', type=str.lower, dest='CONFIG', help="Enter name of config file to search", required=True)
parser.add_argument('-s', '--VALUE', nargs='+', type=str.lower, dest='VALUE', help="Enter values to scan for", required=True)
args = parser.parse_args()
alerts = args.CONFIG
exclusion_values = args.VALUE


with open('pipeline.config', 'r') as f:
    pipeline_config = yaml.load(f)