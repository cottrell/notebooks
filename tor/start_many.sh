#!/bin/bash -e
if [[ $(whoami) != "root" ]]; then
    echo must run as sudo
    exit 1
fi
N=${1:-5}
N=$(($N - 1))
sudo ls > /dev/null 2>&1
for i in $(seq 0 $N); do
    echo "sudo tor -f /etc/tor/torrc.$i > tor.log.$i 2>&1 & echo $! > pid.$i"
    tor -f /etc/tor/torrc.$i > tor.log.$i 2>&1 & echo $! > pid.$i
done
for i in $(seq 0 $N); do
    f=/var/lib/tor_$i/control_auth_cookie
    while [[ ! -e $f ]]; do
        echo file $f does not exist sleep until it does ...
        sleep 1
    done
    echo chmod -R 777 /var/lib/tor_$i
    chmod -R 777 /var/lib/tor_$i
done
