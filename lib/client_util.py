import json
import os

import params

buffer_size = 4096
end_char = b'$'


def send_data(socket, data):
    data += end_char
    while len(data) > 0:
        buffer = data[:buffer_size]
        data = data[buffer_size:]

        if socket.send(buffer) == 0:
            return False

    return True


def receive_data(socket):
    data = b''
    while True:
        buffer = socket.recv(buffer_size)
        data += buffer

        if len(buffer) == 0 or buffer[-1] == end_char[0]:
            break

    data = data[:-1]
    return data


def read_config():
    pt = os.path.join(params.data_dir, 'config.json')
    with open(pt, 'r') as fp:
        data = json.load(fp)
    hostname = data['hostname']
    port = data['port']
    api_key = data['api_key']
    return hostname, port, api_key
