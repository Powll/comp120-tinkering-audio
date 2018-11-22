import wave
import math
import struct
import AudioHelper

import numpy
import scipy
import pygame

# in seconds
LENGTH_OF_FILE_IN_SECONDS = 6

OUTPUT_FILENAME = 'output.wav'

NCHANNELS = 1
SAMPWIDTH = 2
FRAMERATE = 44100
NFRAMES = FRAMERATE * LENGTH_OF_FILE_IN_SECONDS
COMPTYPE = "NONE"
COMPNAME = "NONE"
MAX_VALUE = 32767.0
FREQUENCY = 350
VOLUME = 1

noise_out = wave.open(OUTPUT_FILENAME, 'w')

noise_out.setparams((NCHANNELS,
                     SAMPWIDTH,
                     FRAMERATE,
                     NFRAMES,
                     COMPNAME,
                     COMPTYPE))


def generate_tone(frequency, amplitude):

    values = []

    for i in range(0, NFRAMES):
        value = numpy.sin(
            2.0 * numpy.pi
            * frequency
            * float((i / FRAMERATE)))\
            * amplitude     # maybe replace with parameters?

        values.append(value)

    return values


def sin_wave(position, frequency, amplitude):

    return numpy.sin(
            2.0 * numpy.pi
            * frequency
            * float((position / FRAMERATE)))\
            * MAX_VALUE / amplitude


def get_key(key):
    return AudioHelper.BASE_NOTES(key[0] + '0') * (2 ** int(key[1]))


def combine_tones(*tones):
    """

    """

    values = []

    max_length = 0

    for tone in tones:

        max_length = max(max_length, len(tone))

    for i in range(0, max_length):

        value = 0

        for tone in tones:
            value += tone[i]

        print(str(i), str(value))

        values.append(max(min(MAX_VALUE, value), -MAX_VALUE))

    return values


def package(tone_list):

    values = []

    for i in range(0, len(tone_list)):
        packed_value = struct.pack('h', int(tone_list[i]))
        values.append(packed_value)

    print('Finished packaging')

    return b''.join(values)


pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((100, 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            noise_out.writeframes(
                package(combine_tones(generate_tone(262, 1000), generate_tone(524, 1000))))
            noise_out.close()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            from sys import exit
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            pygame.mixer.music.load('output.wav')
            pygame.mixer.music.play(5, 0.0)

