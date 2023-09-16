import matplotlib.pyplot as p
import numpy as np

from lib.util import compose_rgb
from lib.wave2rgb import wave2rgb

H = 50
N = 85

image = np.zeros((H, N, 3))

for i in range(0, H):
    for j in range(0, N):
        start = 380
        end = 780
        wave = j * (end - start) / N + start
        image[i][j] = wave2rgb(wave)

for i in image[0]:
    color = 255 * i
    color_vector = list(map(lambda x: int(x), color))
    hex_color = compose_rgb(color_vector[0], color_vector[1], color_vector[2])

ax = p.axes()
ax.get_yaxis().set_visible(False)
p.imshow(image)
p.show()
