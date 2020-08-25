#!/bin/sh
# pavucontrol

echo "remember to restart chrome and firefox probably after this."
pulseaudio -k
# not sure which one is needed
pulseaudio --start
sudo alsa force-reload
