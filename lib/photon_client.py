import hashlib
import socket

from lib.client_util import send_data, receive_data, read_config


def get_client(start, end, direction):
    hostname, port, api_key = read_config()
    return PhotonClient(hostname, port, 120, start, end, direction, api_key)


class PhotonClient:
    def __init__(self, host, port, timeout, low, high, direction, api_key):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.settimeout(timeout)

        self.api_hash = hashlib.md5(api_key.encode()).digest()

        self.direction = 0 if direction == 'left' else 1
        self.low = low
        self.high = high
        self.N = high - low + 1

    def __build_header(self, data):
        return data.ljust(16) + self.api_hash

    def reserve(self):
        send_data(self.socket, self.__build_header(b'RESERVE') + b'all')
        res = receive_data(self.socket)
        return res == b'0'

    def apply_color(self, color):
        self.apply([color] * self.N)

    def apply(self, li_hex):
        data = b''

        if self.direction == 0:
            pos = self.low
            for color in li_hex:
                if pos > self.high:
                    break
                data += pos.to_bytes(4, 'little')
                data += color.to_bytes(3, 'little')
                pos += 1
        else:
            pos = self.high
            for color in li_hex:
                if pos < self.low:
                    break
                data += pos.to_bytes(4, 'little')
                data += color.to_bytes(3, 'little')
                pos -= 1

        send_data(self.socket, self.__build_header(b'APPLY') + data)
        res = receive_data(self.socket)
        return res == b'0'

    def keep_alive(self):
        send_data(self.socket, self.__build_header(b'KEEP_ALIVE'))
        res = receive_data(self.socket)
        return res == b'0'
