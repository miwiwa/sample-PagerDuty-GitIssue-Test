#!/bin/bash
#
#  Sends alert with link to failing job to Pager Duty or Git Issue depending on pipeline config
#

enable_alerts=()

# exclude file contains list of alerts not to send
filename="notification.exclude.conf"

# Retrieve line from exclusion list for current job
var=$(grep $IDS_JOB_NAME $filename | sed 's:[^;]*/\(.*\):\1:')
echo "Var: $var"
num=$(echo $var | tr -cd ';' | wc -c)
echo "Num: $num"
# Loop through line and add exclusion to array
for ((i=2;i<=$num+1;i++)); do
        alert_type=$(echo "\"$var"\ | cut -d ";" -f $i"")
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
	/usr/bin/python create_alert.py -a message
elif [[ " ${enable_alerts[@]} " =~ "no-git" ]]; then
	echo "Creating Pager Duty incident and Slack message from wrapper"
	/usr/bin/python create_alert.py -a incident message -s started
elif [[ " ${enable_alerts[@]} " =~ "no-slack" ]]; then
	echo "Creating Pager Duty incident and Git issue from wrapper"
	/usr/bin/python create_alert.py -a incident issue
elif [[ " ${enable_alerts[@]} " =~ "no-pagerduty" ]]; then
	echo "Creating Git issue and Slack message from wrapper"
	/usr/bin/python create_alert.py -a issue message
else
	echo "Creating Pager Duty incident, Slack message, and Git issue from wrapper"
	/usr/bin/python create_alert.py -a incident issue message
fi
