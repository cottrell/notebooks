https://www.hiroom2.com/2017/08/24/ubuntu-1610-nameserver-127-0-0-53-en/
https://askubuntu.com/questions/1012641/dns-set-to-systemds-127-0-0-53-how-to-change-permanently

Adding nameserver 192.168.1.1 to /etc/resolv.conf is necessary. Not sure will survive reboot.


Finally did this, this is an unbelievable amount of noise on this. No idea what they are doing.

    $ cat /etc/network/interfaces
    # interfaces(5) file used by ifup(8) and ifdown(8)
    auto lo
    iface lo inet loopback
    	dns-nameservers 192.168.1.1

