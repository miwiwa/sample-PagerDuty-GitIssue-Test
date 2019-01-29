#!/bin/bash
#
#  Sends alert with link to failing job to Pager Duty or Git Issue depending on pipeline config
#

enable_alerts=()

sudo apt-get update > /dev/null
sudo apt-get install python python-yaml > /dev/null

if [ $# -eq 1 ]
  then
    slack_status=$1
else
  slack_status=="executed"
fi

ids_job_name="Linting"
# exclude file contains list of alerts not to send
filename="pipeline.config"
alert_exclusions="ALERT_EXCLUSIONS"

curl -sSL -u "watkins0@us.ibm.com:${gitApiKey}" "https://raw.github.ibm.com/whc-toolchain/whc-commons/${WHC_COMMONS_BRANCH}/scripts/grab_pipeline_config.py" > grab_pipeline_config.py

get_exclusions=$(python pipeline.py -c $filename -d $alert_exclusions -e)


echo "get_exclusions: $get_exclusions"
# Retrieve line from exclusion list for current job
total_exclusions=$(echo $get_exclusions | tr ',' ' ' | wc -w)

# Loop through line and add exclusions to array
for i in $(seq 1 $total_exclusions); do 
	   alert_type=$(echo "\"$get_exclusions"\ | cut -d "," -f $i"")   
       enable_alerts+=$alert_type
done

# Call python script to send alerts based on content of array
if [[ " ${enable_alerts[@]} " =~ "no-pagerduty" ]] && [[ " ${enable_alerts[@]} " =~ "no-git" ]] && [[ " ${enable_alerts[@]} " =~ "no-slack" ]] ; then
    echo "Alerts not configured for this job"
    exit 0
elif [[ " ${enable_alerts[@]} " =~ "no-pagerduty" ]] && [[ " ${enable_alerts[@]} " =~ "no-slack" ]]; then
	echo "Creating git issue from wrapper"
	/usr/bin/python create_alert.py -a issue
elif [[ " ${enable_alerts[@]} " =~ "no-git" ]] && [[ " ${enable_alerts[@]} " =~ "no-slack" ]]; then
	echo "Creating Pager Duty incident from wrapper"
	/usr/bin/python create_alert.py -a incident
elif [[ " ${enable_alerts[@]} " =~ "no-git" ]] && [[ " ${enable_alerts[@]} " =~ "no-pagerduty" ]]; then
	echo "Creating Slack message from wrapper"
	/usr/bin/python create_alert.py -a message -s $slack_status
elif [[ " ${enable_alerts[@]} " =~ "no-git" ]]; then
	echo "Creating Pager Duty incident and Slack message from wrapper"
	/usr/bin/python create_alert.py -a incident message -s $slack_status
elif [[ " ${enable_alerts[@]} " =~ "no-slack" ]]; then
	echo "Creating Pager Duty incident and Git issue from wrapper"
	/usr/bin/python create_alert.py -a incident issue
elif [[ " ${enable_alerts[@]} " =~ "no-pagerduty" ]]; then
	echo "Creating Git issue and Slack message from wrapper"
	/usr/bin/python create_alert.py -a issue message -s $slack_status
else
	echo "Creating Pager Duty incident, Slack message, and Git issue from wrapper"
	/usr/bin/python create_alert.py -a incident issue message -s $slack_status
fi
