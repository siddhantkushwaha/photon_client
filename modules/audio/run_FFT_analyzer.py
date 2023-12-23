import argparse
import time

import numpy as np

from lib.photon_client import get_client
from modules.audio.stream_analyzer import Stream_Analyzer


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


def wave2rgb(wave):
    gamma = 0.8
    intensity_max = 1

    if wave < 380:
        red, green, blue = 0, 0, 0
    elif wave < 440:
        red = -(wave - 440) / (440 - 380)
        green, blue = 0, 1
    elif wave < 490:
        red = 0
        green = (wave - 440) / (490 - 440)
        blue = 1
    elif wave < 510:
        red, green = 0, 1
        blue = -(wave - 510) / (510 - 490)
    elif wave < 580:
        red = (wave - 510) / (580 - 510)
        green, blue = 1, 0
    elif wave < 645:
        red = 1
        green = -(wave - 645) / (645 - 580)
        blue = 0
    elif wave <= 780:
        red, green, blue = 1, 0, 0
    else:
        red, green, blue = 0, 0, 0

    # let the intensity fall of near the vision limits
    if wave < 380:
        factor = 0
    elif wave < 420:
        factor = 0.3 + 0.7 * (wave - 380) / (420 - 380)
    elif wave < 700:
        factor = 1
    elif wave <= 780:
        factor = 0.3 + 0.7 * (780 - wave) / (780 - 700)
    else:
        factor = 0

    def f(c):
        if c == 0:
            return 0
        else:
            return intensity_max * pow(c * factor, gamma)

    v = f(red), f(green), f(blue)
    v = list(map(lambda x: int(255 * x), v))
    return compose_rgb(v[0], v[1], v[2])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, default=3, dest='device',
                        help='pyaudio (portaudio) device index')
    parser.add_argument('--height', type=int, default=450, dest='height',
                        help='height, in pixels, of the visualizer window')
    parser.add_argument('--n_frequency_bins', type=int, default=85, dest='frequency_bins',
                        help='The FFT features are grouped in bins')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--window_ratio', default='24/9', dest='window_ratio',
                        help='float ratio of the visualizer window. e.g. 24/9')
    parser.add_argument('--sleep_between_frames', dest='sleep_between_frames', action='store_true',
                        help='when true process sleeps between frames to reduce CPU usage (recommended for low update rates)')
    return parser.parse_args()


def convert_window_ratio(window_ratio):
    if '/' in window_ratio:
        dividend, divisor = window_ratio.split('/')
        try:
            float_ratio = float(dividend) / float(divisor)
        except:
            raise ValueError('window_ratio should be in the format: float/float')
        return float_ratio
    raise ValueError('window_ratio should be in the format: float/float')


def run_FFT_analyzer():
    args = parse_args()
    window_ratio = convert_window_ratio(args.window_ratio)

    ear = Stream_Analyzer(
        device=args.device,  # Pyaudio (portaudio) device index, defaults to first mic input
        rate=None,  # Audio samplerate, None uses the default source settings
        FFT_window_size_ms=1000,  # Window size used for the FFT transform
        updates_per_second=1000,  # How often to read the audio stream for new data
        smoothing_length_ms=200,  # Apply some temporal smoothing to reduce noisy features
        n_frequency_bins=args.frequency_bins,  # The FFT features are grouped in bins
        visualize=0,  # Visualize the FFT features with PyGame
        verbose=args.verbose,  # Print running statistics (latency, fps, ...)
        height=args.height,  # Height, in pixels, of the visualizer window,
        window_ratio=window_ratio  # Float ratio of the visualizer window. e.g. 24/9
    )

    client = get_client(11, 85, 'right')
    client.reserve()

    fps = 60  # How often to update the FFT features + display
    last_update = time.time()
    while True:
        if (time.time() - last_update) > (1. / fps):
            last_update = time.time()
            raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()

            data = np.array(binned_fft)
            ndata = (data - np.min(data)) / (np.max(data) - np.min(data))
            ndata = 700 - (250 * ndata)
            li = [wave2rgb(i) for i in ndata]

            client.apply(li)

        elif args.sleep_between_frames:
            time.sleep(((1. / fps) - (time.time() - last_update)) * 0.99)
