# comp-120-tinkering-audio

# Paul Rauca will be working on contract #2

In order to create environment-specific sounds, room-specific variables will be used to determine what kind of sounds to play (leaves rustling, water flowing etc.). For ease of use by a designer, the tool will contain easily editable variables.

# USAGE:

Press 'a' to generate and export a file to /Resources/Audio/Ambient (customizable)
Press 'd' to load and play a sound file, by default -> /Resources/Audio/Ambient/output.wav

USAGE: the following order MUST be respected when calling functions:
export_sound
normalize
halve/double AND/OR echo
append_tone AND/OR combine_tone
generate_tone

When generating tones, feel free to use EITHER frequencies (integers) or notes (strings, e.g. C4)

If you wish to modify what is created, please see the example function in the code and follow the USAGE instructions in the script or in the readme file

The following algorithms were used:

Resampling,
Echoes,
Input/Output,
Tone generation and combination,
Token input