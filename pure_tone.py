import wave
import math
import struct

import numpy
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

    """
    Tone perception:
    
    Human perception relies on ratios of difference rather than absolute values
    e.g. 200 -> 400 Hz and 500 -> 1000 Hz (1:2)
    Intensity is measured as watts per meter squared
    e.g. 0.1 -> 0.01 and 0.001 -> 0.0001
    
    We experience sound in a logarithmic fashion
    Human perception of volume is related to changes in amplitude
    
    See: Logarithmic tables? -> Ed
    
    10 * lg(I1 / I2) I1, I2 - intensities
    
    Normal speech: 60dB
    Shout: 80dB
    
    Weber-Fechner Law: 
    
    """

    values = []

    for i in range(0, NFRAMES):
        value = sin_wave(i, frequency, amplitude)     # maybe replace with parameters?

        values.append(value)

        # print(str(value))

    return values


def generate_tone_square(frequency, amplitude):

    values = []

    for i in range(0, NFRAMES):
        # value = sin_wave(i, frequency, amplitude)     # maybe replace with parameters?
        value = convert_to_simple_square_wave(i, frequency, amplitude)
        values.append(value)

        print(str(value))

        # print(str(value))

    return values


def combine_tones(*tones):

    max_length = 0

    for tone in list(tones):
        if len(tone) > max_length:
            max_length = len(tone)

    print(str(max_length))

    values = []

    for i in range(0, max_length):

        value = 0
        for tone in list(tones):
            if i >= len(tone):
                continue
            else:
                value += tone[i]

            if value > MAX_VALUE:
                values.append(MAX_VALUE)
            elif value < -MAX_VALUE:
                values.append(-MAX_VALUE)
            else:
                values.append(value)

    return values


def superposition(tone_1, tone_2):
    """Reminder: slap Cyrus"""

    values = []

    for i in range(0, max(len(tone_1), len(tone_2))):
        value = tone_1[i] + tone_2[i]

        if value >= MAX_VALUE:
            values.append(MAX_VALUE)
        elif value <= -MAX_VALUE:
            values.append(-MAX_VALUE)
        else:
            values.append(value)

    return values


def convert_to_simple_square_wave(position, frequency, amplitude):

    base_value = math.sin(2 *
                          math.pi *
                          frequency *
                          position /
                          FRAMERATE) * \
                          MAX_VALUE * amplitude

    if base_value < (-MAX_VALUE / 2):
        return -MAX_VALUE
    elif base_value > (MAX_VALUE / 2):
        return MAX_VALUE
    else:
        return 0


def sin_wave(position, frequency, amplitude):

    return math.sin(
            2.0 * math.pi
            * frequency
            * float((position / FRAMERATE)))\
            * MAX_VALUE * amplitude


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
                package(superposition(generate_tone(100, 0.5),
                                      generate_tone(105, 0.5)
                                      )))
            noise_out.close()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            from sys import exit
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            pygame.mixer.music.load('output.wav')
            pygame.mixer.music.play(5, 0.0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            noise_out.writeframes(
                package(generate_tone_square(1760, 0.5))
            )
            noise_out.close()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            noise_out.writeframes(
                package(superposition(superposition(generate_tone(100, 0.5),
                                                    generate_tone(104, 0.5)
                                                    ),
                        generate_tone(102, 0.5)
                                                )))
