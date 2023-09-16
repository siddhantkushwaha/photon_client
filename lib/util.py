def reduce_brightness(color, v):
    r, g, b = split_rgb(color)
    return compose_rgb(int(r * v), int(g * v), int(b * v))


def split_rgb(color):
    red = (color >> 16) & 0b11111111
    green = (color >> 8) & 0b11111111
    blue = color & 0b11111111
    return red, green, blue


def compose_rgb(r, g, b):
    color = 0

    color = color | (r << 16)
    color = color | (g << 8)
    color = color | b

    return color
