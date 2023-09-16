import hashlib
import socket

from lib.client_util import send_data, receive_data


class PhotonClient:
    def __init__(self, host, port, timeout, low, high, api_key):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.settimeout(timeout)

        self.api_hash = hashlib.md5(api_key.encode()).digest()

        self.low = low
        self.high = high

    def __build_header(self, data):
        return data.ljust(16) + self.api_hash

    def reserve(self):
        send_data(self.socket, self.__build_header(b'RESERVE') + b'all')
        res = receive_data(self.socket)
        return res == b'0'

    def apply(self, li_hex):
        pos = self.low
        data = b''
        for color in li_hex:
            data += pos.to_bytes(4, 'little')
            data += color.to_bytes(3, 'little')
            pos += 1
        send_data(self.socket, self.__build_header(b'APPLY') + data)
        res = receive_data(self.socket)
        return res == b'0'

    def keep_alive(self):
        send_data(self.socket, self.__build_header(b'KEEP_ALIVE'))
        res = receive_data(self.socket)
        return res == b'0'
