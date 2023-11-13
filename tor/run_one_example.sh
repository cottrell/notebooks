#!/bin/bash
if [[ $(whoami) != "root" ]]; then
    echo must run as sudo
    exit 1
fi
sudo tor -f /etc/tor/torrc.0 > tor.log.0 2>&1 & echo $! > pid.0
# cat pid.0
# tail -f tor.log.0
