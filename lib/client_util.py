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
