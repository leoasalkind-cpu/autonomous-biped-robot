# USB Microphone

## Hardware
- Raspberry Pi 4
- USB microphone (Texas Instruments PCM2902 Audio Codec)
- USB-A connection

## Setup

Install ALSA recording utilities:

    sudo apt install -y alsa-utils

Check connected microphones:

    arecord -l

## Testing

From the repository root:

    python hardware/microphone/mic_test.py

The script records 5 seconds of audio at:
- 48 kHz
- 16-bit PCM
- Stereo (2 channels)

Output: /tmp/mic_test.wav

To specify a different microphone or duration:

    python hardware/microphone/mic_test.py --device plughw:3,0 --duration 10

Note: ALSA card numbers may change after reboot.
Check `arecord -l` to find the current card number.

## Current Status

- USB device detected successfully
- Audio recording verified
- WAV file validated
- Speech playback tested successfully

## Future ROS 2 Integration

Create an audio capture node to publish microphone
data for speech recognition and voice-command processing.
