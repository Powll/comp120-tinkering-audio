# Dictionary of base notes and their respective frequencies

BASE_NOTES = dict(
    C0=16.35,
    CS=17.32,
    D0=18.35,
    DS=19.45,
    E0=20.60,
    F0=21.83,
    FS=23.12,
    G0=24.50,
    GS=25.96,
    A0=27.50,
    AS=29.14,
    B0=30.87
)

# Dictionary containing the ambient sound types:

AMBIENT_SOUND_TYPES = dict(
    custom='custom',
    wind=dict(
        calm='wind_calm',
        storm='wind_storm'
    ),
    water=dict(
        flowing='water_flowing',
        waterfall='water_waterfall'
    )
)

# Dictionary for supported formats and the required packaging:

AUDIO_FORMAT = dict(
    wav=dict(
        pack_method='h',
        extension='.wav'
    ),
    ogg=dict(
        pack_method='',
        extension='.ogg'
    ),
)

# Arguments used in exporting audio files

OUTPUT_FILENAME = 'output'  # Default name used in exporting
OUTPUT_DIRECTORY = './Resources/Audio/Ambient/'  # Default directory

# Arguments used in importing audio files

INPUT_FILENAME = 'input'
INPUT_DIRECTORY = './Resources/Audio/Imports/'
