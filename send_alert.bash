#!/bin/bash
#
#  Sends alert with link to failing job to Pager Duty or Git Issue depending on pipeline config
#

enable_alerts=()



sudo apt-get update
sudo apt-get install python python-yaml

if [ $# -eq 1 ]
  then
    slack_status=$1
else
  slack_status=="executed"
fi


# exclude file contains list of alerts not to send
#filename="notification.exclude.conf"
filename="pipeline.config"
echo "filename: $filename"
echo "About to curl"
curl -sSL -u "watkins0@us.ibm.com:${gitApiKey}" "https://raw.github.ibm.com/whc-toolchain/whc-commons/${WHC_COMMONS_BRANCH}/scripts/grab_pipeline_config.py" > grab_pipeline_config.py

var=$(python grab_exclusions.py -c $filename | sed 's/'[][]'//g')
echo "var: $var"

# Retrieve line from exclusion list for current job
#var=$(grep $IDS_JOB_NAME $filename | sed 's:[^;]*/\(.*\):\1:')
#echo "var: $var"
num=$(echo $var | tr -cd ',' | wc -c)
echo "num: $num"
# Loop through line and add exclusion to array
for ((i=1;i<=$num+1;i++)); do
       alert_type=$(echo "\"$var"\ | cut -d "," -f $i"")
       
       echo "alert_type: $alert_type"
       enable_alerts+=$alert_type
done

for ((i=0; i<${#enable_alerts[@]}; i++)); do
    eval(alerts=${enable_alerts[i]}
    print(alerts)
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
