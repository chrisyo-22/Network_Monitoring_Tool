# Network Monitoring Tool

# To run on mininet
```
ssh mininet@....

sudo python3 -m pip install -r requirements.txt
sudo mn
h1 sudo python3 capture.py > capture.log &

# testing UDP
h1 sudo python3 udp_server.py &
h2 sudo python3 udp_client.py &
```
