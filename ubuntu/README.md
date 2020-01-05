# WIFI

    lshw
    lsusb -vv -d 2357:010e
    ip link
    journalctl -xe
    cat /var/log/syslog | grep network
    # THIS DID IT LAST TIME?
    sudo dhclient
    sudo ip link set enx503eaa4de20b up
    # and then toggling the network ... arg

    # another attempt seems like dhclient lease renewal did it

    journalctl --follow

    option ) powersave 2 instead of 3 in     /etc/NetworkManager/conf.d/default-wifi-powersave-on.con


    option) GOing to try removing netork manager and install wicd:

    sudo apt install wicd-gtk
    sudo apt remove network-manager-gnome network-manager
    sudo dpkg --purge network-manager-gnome network-manager



    smtp
    relay.plus.net

# network

    mtr www.google.co.uk
