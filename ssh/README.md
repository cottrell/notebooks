# Tunnel

    ssh -N -f -L localhost:8443:localhost:8443 192.168.1.9
    ssh -N -L localhost:8443:localhost:8443 192.168.1.9


Remember if you have a single port exposed (forwarded on router) for ssh. You can still open up a ssh tunnel via:

    ssh -p FWD_PORT -v -N -f -L localhost:PORT:localhost:PORT username@ip
