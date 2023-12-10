# Network Monitoring Tool

```
# To run on mininet vm
ssh mininet@....

# install packages
sudo python3 -m pip install -r requirements.txt

# start mininet using default topology
sudo mn

# To start capturing on host h1
h1 ./run.sh captured.log metrics.log

# To stop capturing on host h1
h1 ./stop.sh <pid>

# testing UDP
h1 python3 lib/test/udp_server.py &
h2 python3 lib/test/udp_client.py &

# testing TCP
h1 python3 lib/test/http_server.py &
h2 wget http://10.0.0.1:3946
```
