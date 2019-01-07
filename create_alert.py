#!/usr/bin/env python
# Program submits PagerDuty incidents or Git issues upon request

import pip
package = 'requests'
pip.main(['install', package])

import requests
import json
import argparse
from os import environ
import subprocess
import re
import sys

# Read in argument(s)
description = 'Specify creation of incident/issue in Pagerduty and Git Issues'
   
parser = argparse.ArgumentParser(     description=__doc__)
parser.add_argument('-a','--ALERTS', nargs='+', type=str.lower, dest='ALERTS', help="Enter 'PagerDuty' and/or 'Git' to open incident/issue", required=True)

args = parser.parse_args()
alerts = args.ALERTS

# Import Pipeline environment variables 
ids_job_name = environ.get('IDS_JOB_NAME')
ids_job_id = environ.get('IDS_JOB_ID')
ids_stage_name = environ.get('IDS_STAGE_NAME')
ids_project_name = environ.get('IDS_PROJECT_NAME')
git_url = environ.get('GIT_URL')
archive_dir = environ.get('ARCHIVE_DIR')
pipeline_id = environ.get('PIPELINE_ID')
pipeline_stage_id = environ.get('PIPELINE_STAGE_ID')
workspace = environ.get('WORKSPACE')
github_token = environ.get('gitApiKey')
     
# Load toolchain json to dict for parsing
toolchain_json = "%s/_toolchain.json" % workspace

with open(toolchain_json) as f:
    data = json.load(f)

ids_region_id = data['region_id']
instance_id = [i['instance_id'] for i in data["services"] if 'pipeline' in i['broker_id']]
ids_instance_id = instance_id[0]

pipeline_base_url = "https://console.bluemix.net/devops/pipelines/" 
pipeline_full_url = pipeline_base_url + pipeline_id + "/" + pipeline_stage_id +  "/" + ids_job_id + "?env_id=" + ids_region_id

def trigger_incident():
	# Function creates request to create new PagerDuty incident and submits
    
    # Parse dict for PagerDuty parameters
    try:
        pd_service_id = [i['parameters']['service_id'] for i in data["services"] if 'pagerduty' in i['broker_id']]
        pd_api_key = [i['parameters']['api_key'] for i in data["services"] if 'pagerduty' in i['broker_id']]
        pd_user_email = [i['parameters']['user_email'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    	
        api_key = pd_api_key[0]
        service_id = pd_service_id[0]
        user_email = pd_user_email[0]
    except (KeyError, IndexError):
        print("ERROR: Pager Duty is not configured with the toolchain")
        return 1
     
	# Develop request to create incident through API
    url = 'https://api.pagerduty.com/incidents'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=api_key),
        'From': user_email
    }

    payload = {
        "incident": {
            "type": "incident",
            "title": "Job: " + ids_job_name + " in Stage: " + ids_stage_name + " and Project: " + ids_project_name + " failed" ,
            "service": {
                "id": service_id,
                "type": "service_reference"
            },
            "body": {
                "type": "incident_body",
                "details":  pipeline_full_url
            }
          }
        }
	
	# Send request to PagerDuty
    print("Creating PagerDuty incident")
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    
    code=r.status_code
    
    # Check if request was successful. If not successful then fail the job   
    if code != 201:
    	print("ERROR: PagerDuty incident request did not complete successfully due to error code:", code)
        exit()
    else:
		print("PagerDuty incident request created successfully")
		
def trigger_issue():
    # Function creates request to create Git Issue and submits
    git_repo_owner = environ.get('git_repo_owner')
    git_repo_name = environ.get('git_repo_name')
    git_issue_label = environ.get('git_issue_label')
    
    api_base_url = "https://api.github.ibm.com/"
    
    # Check to see if env vars populated for repo owner and name. If not, parse git_url if git was input to job.  Otherwise
    # parse the _toolchain.json file for values. If they don't exist there then Git issues must not be integrated.
    if git_repo_owner is not None and git_repo_name is not None:
      print("Creating Git issue....")
    elif git_url is not None:
      print("Creating Git issue....")
      git_repo_name = re.search(r'(.*)/(.*)', git_url).group(2).split('.')[0]
      git_repo_owner = re.search(r'(.*)/(.*)', git_url).group(1).split('/')[3]
    else:
      try:
        print("Creating Git issue....")
        git_repo_owner = [i['parameters']['owner_id'] for i in data["services"] if 'git' in i['broker_id']]
        git_repo_name = [i['parameters']['repo_name'] for i in data["services"] if 'git' in i['broker_id']]
      except (KeyError, IndexError):
        print("ERROR: Git Issues is not configured correctly with the toolchain")
        return 1
    
    # If label value isn't passed in by user default to 'bug'
    if git_issue_label is None:
      git_issue_label = 'bug'

    # Define title of Git issue, headers, and issue content    
    issue_title = "Job: " + ids_job_name + " in Stage: " + ids_stage_name + " and Project: " + ids_project_name + " failed"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "token " + github_token
    }

    issue = {'title': issue_title,
             'body': pipeline_full_url,
             'labels': [git_issue_label]}
    
    # Specifies URL for github api
    url = api_base_url + "repos/" + git_repo_owner + "/" + git_repo_name + "/issues"
    
    # Send request to github.ibm.com
    r = requests.post(url, headers=headers, data=json.dumps(issue))
  	
    if r.status_code != 201:
        raise SystemError("'ERROR: Could not create Git Issue {0:s}'.format(title) due to", r.status_code)
    else:
        print ('Successfully created Git issue: {0:s}'.format(issue_title))

def trigger_slackMessage():
    headers = {
        'Content-type': 'application/json',
    }
    d = {}
    d['text'] = "Job: " + ids_job_name + "started in Stage: " + ids_stage_name
    print("d:", d)
    data = json.dumps(d)
    print(data)
    web_hook_url = 'https://hooks.slack.com/services/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'
   # data = '{"text": "JOB NAME", ids_job_name, "started in STAGE: ", ids_stage_name}'
   #data = '{"text":"Hello, World!", + }'
    response = requests.post(web_hook_url, headers=headers, data=data)

    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )

if __name__ == '__main__':	

    if all(alert_type in alerts for alert_type in ('incident', 'issue', 'message')):		
        print("=============================")
        print("Creating Pager Duty incident and GitHub issue")
        trigger_incident()	
        trigger_issue()
        trigger_slackMessage()
    elif all(alert_type in alerts for alert_type in ('incident', 'issue')):
        print("=============================")
        print("Creating Pager Duty incident and GitHub issue")
        trigger_incident()	
        trigger_issue()
    elif all(alert_type in alerts for alert_type in ('incident', 'message')):
        print("=============================")
        print("Creating Pager Duty incident and Slack Message")
        trigger_incident()	
        trigger_slackMessage()
    elif all(alert_type in alerts for alert_type in ('issue', 'message')):
        print("=============================")
        print("Creating Git Issue and Slack Message")
        trigger_issue()	
        trigger_slackMessage()
    elif 'incident' in alerts:
        print("=============================")
        print("Creating Pager Duty incident")
        trigger_incident()
    elif 'issue' in alerts:
        print("=============================")
        print("Creating GitHub issue")
        trigger_issue()
    elif 'slackMessage' in alerts:
        print("=============================")
        print("Creating Slack message")
        trigger_slackMessage()       
    else:
        print("ERROR: Alert type was not specified in call")

	
