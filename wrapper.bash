#!/bin/bash

pwd
ls -la

filename="notification.exclude.conf"
echo "IDS_JOB_NAME: ${IDS_JOB_NAME}"

var=$(grep $IDS_JOB_NAME $filename | sed 's:[^;]*/\(.*\):\1:')
echo "var: $var"
num=$(echo $var | tr -cd ';' | wc -c)

for ((i=2;i<=$num+1;i++)); do
        echo "\"$var"\ | cut -d ";" -f $i""
done

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

