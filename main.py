import sys
from scapy.all import *

while True:
    sniff(iface="lo0", prn = lambda x:x.show())