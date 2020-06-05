#!/bin/sh
# pavucontrol

# pulseaudio -k
# sudo alsa force-reload

pulseaudio -k && pulseaudio --start
