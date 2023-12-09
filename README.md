# Network Monitoring Tool

# To run on mininet
```
ssh mininet@....

cd lib
sudo python3 -m pip install -r requirements.txt
sudo mn
h1 sudo python3 capture.py > capture.log &

# testing UDP
h1 python3 test/udp_server.py &
h2 python3 test/udp_client.py &

# testing TCP
h1 python3 test/http_server.py &
h2 wget http://10.0.0.1:3946
```
