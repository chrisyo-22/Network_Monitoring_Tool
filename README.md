# Network Monitoring Tool

### Monitoring on Linux machine
```
# install packages
sudo python3 -m pip install -r requirements.txt

# To start capturing (feel free to change the log file name)
# root privileges is required due to the extensive use of raw sockets
sudo bash ./run.sh captured.log metrics.log
# Packets captured will be logged to captured.log
# System metrics will be calculated and logged to metrics.log every 5 seconds
# You can change the calculation frequency in capture.py by modifying the UPDATE flag.

# To stop capturing
sudo bash ./stop.sh <pid>
# This will stop both capturing and metrics calculations
```

### Monitoring and testing on Mininet vm
```
# Using Mininet allow us to emulate network conditions to test the 
# correctness of this monitoring tool by examining the output in the log files.
ssh mininet@...

# install packages
sudo python3 -m pip install -r requirements.txt

# start mininet using default topology
sudo mn

# To start capturing on host h1
h1 ./run.sh captured.log metrics.log

# To stop capturing on host h1
h1 ./stop.sh <pid>

# To test ARP and ICMP
h1 ping -c 1 h2
h2 ping -c 1 h1

# To test UDP
h1 python3 lib/test/udp_server.py &
h2 python3 lib/test/udp_client.py &
# h2 would send one UDP packet to h1 every second
# h1 would reply upon receiving a packet
# You can change the send frequency in /lib/test/udp_client.py
# You should begin to see metrics for this process in metrics.log

# To test TCP
h1 python3 lib/test/http_server.py &
h2 wget http://10.0.0.1:3946
# You should begin to see metrics for this process in metrics.log

# metrics for exited processes would be cleaned up (ie. stop printing metrics) in 10 seconds 
```
