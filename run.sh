#!/bin/bash

# Set default file names
sniffed_packets_file="sniff.log"
process_network_data_file="proc.log"

# Override default file names if arguments are provided
if [ "$#" -eq 2 ]; then
    sniffed_packets_file=$1
    process_network_data_file=$2
elif [ "$#" -ne 0 ]; then
    echo "Usage: $0 [<sniffed_packets_file> <process_network_data_file>]"
    echo "       If no files are specified, defaults to sniff.log and proc.log"
    exit 1
fi

# Run monitoring_begin.py in the background and redirect output to run.log
nohup python3 monitoring_begin.py "$sniffed_packets_file" "$process_network_data_file" > run.log 2>&1 &

# Get the PID of the background process
pid=$!
echo "Monitoring started as PID: $pid"
echo "Output or error logged to run.log"
echo "Sniffed Packet Data will go to $sniffed_packets_file"
echo "Process Network Stats will go to $process_network_data_file"
echo "Stop the monitoring by >>> sudo bash ./stop.sh $pid"

# Exit the script
exit 0
