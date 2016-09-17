sudo mavproxy.py --master=/dev/ttyAMA0 --baudrate=115200 --out=udp:ec2-54-172-141-80.compute-1.amazonaws.com:5760 --out=127.0.0.1:14550 --daemon > mavbridge.log &
