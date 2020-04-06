# WIFI

    lsusb
    cat /etc/network/interfaces
    iwconfig


ALTERNATIVE TO TRACEROUTE mtr

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


# 2020-04-04

lsusb
https://www.tp-link.com/uk/support/download/archer-t4uh/

Trying:
https://github.com/Red-Eyed/TP-LINK_Archer_T4U_v3

https://community.tp-link.com/en/home/stories/detail/323

lsmod | grep 882xbu # was already there?
88x2bu               2613248  0
modprobe -f 88x2bu
88x2bu               2613248  0
    # check  the ko file is in latest
lr /lib/modules/5.3.0-42-generic/kernel/drivers/net/wireless/
add 88x2bu to /etc/modules

check with iwconfig

sudo service network-manager force-reload

https://forums.linuxmint.com/viewtopic.php?t=273297

# 2020-04-05

now trying 
git clone https://github.com/lwfinger/rtl8188eu.git
cd rtl8188eu
make all
sudo make install
sudo systemctl reboot
