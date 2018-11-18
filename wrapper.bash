#!/bin/bash

pwd
ls -la

filename="notification.exclude.conf"
echo "IDS_JOB_NAME: ${IDS_JOB_NAME}"

echo "entering while loop"
echo "filename: $filename"

while read line; do
	echo "$line"
  	if [[ $line =~ ${IDS_JOB_NAME} ]] ; then 
  		alert=$(cut -d ";" -f 2 <<< $line)
  		echo "alert: $alert"
  		echo "Inside if statement in while loop"
  	else
  		echo "inside else statement"
  		echo "Job Name not found in exclusion list"
  	fi
done <${filename}

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

