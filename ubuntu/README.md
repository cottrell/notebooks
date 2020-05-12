# 2020-04-07

    lsusb # this should appear
    iwconfig # this might be missing

https://askubuntu.com/questions/1224074/no-wifi-adapter-found-in-gnome-control-center/1225019#1225019

    dkms status
    # sudo dkms remove modname/version # do this for all present
    sudo dkms remove 8812au/4.2.2 --all

    git clone https://github.com/gnab/rtl8812au.git
    cd rtl8812au
    sudo rsync -rvhP ./ /usr/src/8812au-4.2.2
    sudo dkms add -m 8812au -v 4.2.2
    sudo dkms build -m 8812au -v 4.2.2
    sudo dkms install -m 8812au -v 4.2.2
    sudo modprobe 8812au


After reboot needed to launch wicd-client to select network. Does not need to stay open apparently.

See `old/` for previous notes.

Remember to keep wifi on in power save mode. Go to settings.
