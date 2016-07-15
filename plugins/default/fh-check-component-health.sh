#!/bin/bash
######################################################################
#
# Nagios Plugin to check the health of a component and associated systems.
#
# Author: Peter Braun <pbraun@redhat.com>
#
######################################################################

PATH=$PATH:/usr/local/bin

HOST=$1
PORT=$2

status=0

JSON=$(curl -q http://${HOST}:${PORT}/sys/info/health 2> /dev/null)

#test the JSON is valid
echo $JSON | jq "." &>/dev/null
if [ $? -ne 0 ]; then
  echo "Error parsing JSON:"
  echo $JSON
  exit 3
fi

#Check overall status
if [ $(echo $JSON | jq -r ".status") != "ok" ]; then
  echo "Component is not OK ("$(echo $JSON | jq -r ".status")")"
  echo $JSON | jq -r ".summary"
  echo $JSON | jq -r '.details[] | select(.test_status != "ok")'
  status=2
fi

if [ $status -eq 0 ]; then
  echo "All systems operating normally."
fi
exit $status