#!bin/python
from json import dumps as to_json
from re import search
from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
import os
import signal


class Parser():
    def __init__(self, source_file: str):
        self.pattern = "[0-9]+,[a-zA-Z]+,[0-9]+.[0-9]+,[0-9]+.[0-9]+"
        self.file = source_file

    def __del__(self):
        pass

    def valid_syntax(self, line: str) -> bool:
        return search(self.pattern, line)

    def parse(self) -> str:
        msg = []
        with open(self.file, 'r') as file:
            for line in file:
                clean_line = line.strip()
                if self.valid_syntax(clean_line):
                    data = clean_line.split(',')
                    coin = {'id': data[0],
                            'value1': data[2],
                            'value2': data[3],
                            'name': data[1]}
                    msg.append(coin)
        return to_json(msg)


class Publisher():
    def __init__(self):
        self.ip = "localhost"
        self.port = 10000

    def publish(self, msg: str):
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.sendto(bytes(msg, "utf-8"), (self.ip, self.port))


def signal_handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise OSError("Program ended by external signal")


def main():
    config = dict()
    with open('config.txt', 'r') as config_file:
        for line in config_file:
            c = line.strip().split('=')
            key = c[0]
            val = c[1]
            config[key] = val

    parser = Parser(config['file_path'] + config['file_name'])
    publisher = Publisher()

    while True:
        msg = parser.parse()
        print(msg)
        publisher.publish(msg)
        sleep(30)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    try:
        main()
    except OSError as e:
        print(e)
