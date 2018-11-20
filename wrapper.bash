#!/bin/bash

enable_alerts=()

filename="notification.exclude.conf"
echo "IDS_JOB_NAME: ${IDS_JOB_NAME}"

echo "Downloading tarball from Artifactory"
$(curl -H 'X-JFrog-Art-Api:${artifactory_apikey}' -O "https://na.artifactory.swg-devops.com/artifactory/wh-itops-rhel-7-supplementary-rpm-local/https://na.artifactory.swg-devops.com:443/artifactory/wh-itops-rhel-7-supplementary-rpm-local/OVMF-20160608b-1.git988715a.el7.noarch.rpm")

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
	/usr/bin/python create_alert.py -a issue
elif [[ " ${enable_alerts[@]} " =~ "no-git" ]]; then
	echo "Creating Pager Duty incident from wrapper"
	/usr/bin/python create_alert.py -a incident
else
	echo "Creating both Pager Duty incident and Git issue from wrapper"
	/usr/bin/python create_alert.py -a incident issue
fi

