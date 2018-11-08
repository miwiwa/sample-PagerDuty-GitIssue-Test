#!/bin/bash

executable_script=$1
incident=$2
issue=$3

echo "executable script: $executable_script"

qa_test="$(node $executable_script lint)"

if [[ $? != 0 ]]
then
	/usr/bin/python create_alert.py -a $incident $issue
else
	echo "tests passed"
fi

echo "qa_test: $qa_test"

