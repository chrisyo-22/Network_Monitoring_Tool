#!/bin/bash

# Check if a process ID is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pid>"
    exit 1
fi

input_pid=$1

# Find PIDs of the running instances of the monitoring script
pids=$(pgrep -f monitoring_begin.py)

# Check if the input PID is in the list of PIDs
if [[ $pids =~ (^|[[:space:]])$input_pid($|[[:space:]]) ]]; then
    echo "Sending Stop Signal to monitoring script with PID $input_pid"
    kill -SIGINT $input_pid
    while kill -0 $input_pid 2>/dev/null; do
        sleep 1
    done

    echo "Script finished"
else
    echo "No monitoring script is running with PID $input_pid"
    exit 1
fi
