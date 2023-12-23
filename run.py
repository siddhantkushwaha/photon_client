import colorsys
import time

from lib.photon_client import get_client
from lib.util import reduce_brightness, compose_rgb


def test():
    client_socket = get_client(11, 96, 'right')
    client_socket.reserve()
    client_socket.apply_color(reduce_brightness(0xff00ff, 1))

    while True:
        time.sleep(10)
        client_socket.keep_alive()


def aurora_effect(led_strip_size, speed=0.1):
    client_socket = get_client(11, 96, 'right')
    client_socket.reserve()

    frame = [0] * led_strip_size

    # Function to interpolate in the HSV color space
    def lerp_hsv(hsv1, hsv2, t):
        return tuple(a + (b - a) * t for a, b in zip(hsv1, hsv2))

    # Define the aurora colors in HSV
    aurora_colors = [(0.25, 0.8, 0.8),  # Greenish
                     (0.58, 0.8, 0.8),  # Blueish
                     (0.75, 0.8, 0.8)]  # Purpleish

    def calculate_color(position, time_offset):
        # Calculate effective position with time offset
        effective_position = (position + time_offset) % 1

        # Determine the indices of the colors for interpolation
        color_index = int(effective_position * len(aurora_colors))
        next_color_index = (color_index + 1) % len(aurora_colors)

        # Calculate interpolation factor
        local_pos = (effective_position * len(aurora_colors)) % 1

        # Interpolate between two adjacent colors in HSV
        color1 = aurora_colors[color_index]
        color2 = aurora_colors[next_color_index]
        hsv_interpolated = lerp_hsv(color1, color2, local_pos)

        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(*hsv_interpolated)]
        return r, g, b

    while True:
        # Use the current time to calculate the time offset
        time_offset = (time.time() * speed) % 1

        for i in range(led_strip_size):
            color = calculate_color(i / led_strip_size, time_offset)
            # set_color(i, color)
            frame[i] = compose_rgb(*color)

        # show()
        client_socket.apply(frame)
        time.sleep(0.05)


if __name__ == '__main__':
    aurora_effect(86, speed=0.2)
