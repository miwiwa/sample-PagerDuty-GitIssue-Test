#!/bin/bash

enable_alerts=()

filename="notification.exclude.conf"
echo "IDS_JOB_NAME: ${IDS_JOB_NAME}"

var=$(grep $IDS_JOB_NAME $filename | sed 's:[^;]*/\(.*\):\1:')
echo "var: $var"
num=$(echo $var | tr -cd ';' | wc -c)

for ((i=2;i<=$num+1;i++)); do
        alert_type=$(echo "\"$var"\ | cut -d ";" -f $i"")
        enable_alerts+=$alert_type
done

if [[ " ${enable_alerts[@]} " =~ "no-pagerduty" ]] && [[ " ${enable_alerts[@]} " =~ "no-git" ]] ; then
    echo "PagerDuty and Git Issues not configured for this job"
    exit 0
elif [[ " ${enable_alerts[@]} " =~ "no-pagerduty" ]]; then
	echo "Creating git issue from wrapper"
	/usr/bin/python create_alert.py -a $issue
elif [[ " ${enable_alerts[@]} " =~ "no-git" ]]; then
	echo "Creating Pager Duty incident from wrapper"
	/usr/bin/python create_alert.py -a $incident
else
	echo "Creating both Pager Duty incident and Git issue from wrapper"
	/usr/bin/python create_alert.py -a $incident $issue
fi

#executable_script=$1
#incident=$2
#issue=$3

#echo "executable script: $executable_script"

#qa_test="$(node $executable_script lint)"

#if [[ $? != 0 ]]
#then
#	/usr/bin/python create_alert.py -a $incident $issue
#else
#	echo "tests passed"
#fi

