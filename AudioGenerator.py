import wave
import math
import struct
import AudioHelper

import numpy
import scipy
import types
import pygame
from pathlib import Path

from AudioHelper import AMBIENT_SOUND_TYPES,\
    AUDIO_FORMAT, \
    OUTPUT_DIRECTORY,\
    OUTPUT_FILENAME, \
    INPUT_FILENAME, \
    INPUT_DIRECTORY

# TODO: format all the functions below into a single Audio class

# in seconds
LENGTH_OF_FILE_IN_SECONDS = 6

# TODO: move constants to AudioHelper

NCHANNELS = 1
SAMPWIDTH = 2
FRAMERATE = 44100
NFRAMES = FRAMERATE * LENGTH_OF_FILE_IN_SECONDS
COMPTYPE = "NONE"
COMPNAME = "NONE"
MAX_VALUE = 32767.0
FREQUENCY = 350
VOLUME = 1


def import_sound(file_path=INPUT_DIRECTORY,
                 file_name=INPUT_FILENAME + AUDIO_FORMAT['wav']['extension'],
                 file_format='wav',
                 operation='r'):
    """
    Returns an audio object based on given arguments
    :param file_name: name of file, INCLUDING extension
    :param file_path: path of file, EXCLUDING self
    :param file_format: format of file (e.g. ".wav")
    :param operation: supported arguments: "w", "r", "wb", "rb"
    :return: a readable/writeable audio file
    """

    try:

        if Path(file_path + file_name).exists():
            try:

                if AUDIO_FORMAT[file_format]['extension']\
                        == AUDIO_FORMAT['wav']['extension']:
                    return wave.open(file_path + file_name, operation)

            except ImportError:

                raise Exception('File format',
                                '.' + file_format,
                                'not supported')

    except FileNotFoundError:

        print('File',
              file_path + file_name + '.' + file_format,
              'not found')


def export_sound(tone,
                 file_path=OUTPUT_DIRECTORY,
                 file_name=OUTPUT_FILENAME + AUDIO_FORMAT['wav']['extension'],
                 file_format='wav',
                 file_params=(NCHANNELS,
                              SAMPWIDTH,
                              FRAMERATE,
                              NFRAMES,
                              COMPNAME,
                              COMPTYPE)
                 ):

    """
    Exports an audio file in a given format
    :param tone: list of tone to be exported
    :param file_path: directory to export to
    :param file_name: name of exported file
    :param file_format: format of exported file
    :param file_params: parameters of exported file
    """

    export = wave.open(file_path + file_name, 'wb')

    export.setparams(file_params)

    export.writeframes(
        package(
            tone, AUDIO_FORMAT[file_format]['pack_method']
        )
    )

    export.close()


def adsr_envelope(tone,
                  peak_level,
                  attack_time,
                  decay_time,
                  sustain_level,
                  sustain_time,
                  release_time,
                  ):
    # TODO: implement this function, separately or within the sine wave
    pass


def echo(filename, delay):
    s1 = wave.open(filename, "r")


def generate_tone(frequency, amplitude, wave_type='sine'):

    values = []

    if isinstance(frequency, str):
        frequency = get_key(frequency)

    for i in range(0, NFRAMES):
        value = \
            triangle_wave(i, frequency, amplitude) if 'triangle' in wave_type\
            else sin_wave(i, frequency, amplitude)

        values.append(value)

    return values


def samples(tone):

    return range(0, len(tone))


def normalize(tone):
    """
    Normalizes a given tone
    :param tone: the tone to be normalized
    :return: a normalized tone
    """
    max_value = max(tone)

    modifier = float(MAX_VALUE / max_value)

    for i in samples(tone):
        tone[i] *= modifier

    return tone


def sin_wave(position, frequency, amplitude):

    return numpy.sin(
            2.0 * numpy.pi
            * frequency
            * float((position / FRAMERATE)))\
            * MAX_VALUE / amplitude


def triangle_wave(position, frequency, amplitude):

    return ((2.0 * amplitude) / numpy.pi) *\
        numpy.arcsin(numpy.sin((2.0 * numpy.pi * position) / frequency))


def get_key(key):

    """
    Returns the corresponding frequency of a note in Hz
    :param key: string containing the note and the level e.g. C7
    :return: (int) frequency in Hz
    """

    return int(AudioHelper.BASE_NOTES[key[0] + '0'] * (2 ** int(key[1]))) + 1


def combine_tones(*tones):

    # TODO: add docstring

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


def package(tone, package_type='h'):

    # TODO: add docstring, add support for multiple tones(?)

    values = []

    for i in range(0, len(tone)):
        packed_value = struct.pack(package_type, int(tone[i]))
        values.append(packed_value)

    print('Finished packaging')

    return b''.join(values)


pygame.init()
pygame.display.init()

screen = pygame.display.set_mode((100, 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            export_sound(normalize(combine_tones(generate_tone(110, 1000), generate_tone(112, 1000))))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            from sys import exit
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            pygame.mixer.music.load('./Resources/Audio/Ambient/output.wav')
            pygame.mixer.music.play(5, 0.0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            print(str(get_key('C5')))

