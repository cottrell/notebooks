# WIFI PROBLEMS

## 2021-04

    * lsusb was ok
    * iwconfig showed WIFI entry
    * nothing was showing in wifi app, dongle light was not blinking
    * ran ./bounce_wifi.sh and it started working

Had issues with network, could not sudo apt-get update for instance. Unplugging and plugging in wifi adapter *maybe* suddently improved things. Not sure.

## 2021-01

    lsusb | grep TP
    Bus 001 Device 006: ID 2357:010e TP-Link TL-WN722N v2

    # but iwconfig shows no wireless connection
    # uninstall all dkms ... manually get versions
    dkms status
    sudo dkms remove 8812au/4.2.3 --all
    sudo dkms remove rtl8812au/4.3.8.12175.20140902+dfsg --all

    # then rebuild
    git clone https://github.com/gnab/rtl8812au.git
    cd rtl8812au
    # I HAVE NO IDEA HOW TO PICK THE VERSION, see the readme for dev setup installs
    sudo make dkms_install

    # THEN REBOOT?

    Yes this worked.

    # NOT THIS?
    # sudo rsync -rvhP ./ /usr/src/8812au-$VERSION
    # sudo dkms add -m 8812au -v $VERSION
    # sudo dkms build -m 8812au -v $VERSION
    # sudo dkms install -m 8812au -v $VERSION
    # sudo dkms status
    # # auto load at boot
    # echo 8812au | sudo tee -a /etc/modules
    # sudo modprobe 8812au


## 2020-04-07

    lsusb # this should appear TP-Link or something like that
    iwconfig # this might be missing

## If device shows but network manager not working

    $ systemctl status NetworkManager.service
    ● NetworkManager.service - Network Manager
         Loaded: loaded (/lib/systemd/system/NetworkManager.service; enabled; vendor preset: enabled)
         Active: failed (Result: exit-code) since Sun 2020-07-26 16:29:23 BST; 3min 19s ago
           Docs: man:NetworkManager(8)
        Process: 20365 ExecStart=/usr/sbin/NetworkManager --no-daemon (code=exited, status=1/FAILURE)
       Main PID: 20365 (code=exited, status=1/FAILURE)

Reminder wicd is deprecated.

    $ sudo /usr/sbin/NetworkManager -d

## Use snap!

https://docs.ubuntu.com/core/en/stacks/network/network-manager/docs/installation

snap connections network-manager

## Reinstalling drivers

https://askubuntu.com/questions/1224074/no-wifi-adapter-found-in-gnome-control-center/1225019#1225019

    dkms status
    # sudo dkms remove modname/version # do this for all present
    # WATCH FOR VERSION BUMPS THIS IS JUST AN EXAMPLE
    # WATCH FOR VERSION BUMPS THIS IS JUST AN EXAMPLE
    # WATCH FOR VERSION BUMPS THIS IS JUST AN EXAMPLE
    # WATCH FOR VERSION BUMPS THIS IS JUST AN EXAMPLE
    VERSION=4.2.3
    sudo dkms remove 8812au/$VERSION --all

    git clone https://github.com/gnab/rtl8812au.git
    cd rtl8812au
    # SEE THE README!!!!!!!!!!!!!!
    sudo rsync -rvhP ./ /usr/src/8812au-$VERSION
    sudo dkms add -m 8812au -v $VERSION
    sudo dkms build -m 8812au -v $VERSION
    sudo dkms install -m 8812au -v $VERSION
    sudo dkms status
    # auto load at boot
    echo 8812au | sudo tee -a /etc/modules
    sudo modprobe 8812au


After reboot needed to launch wicd-client to select network. Does not need to stay open apparently.

See `old/` for previous notes.

Remember to keep wifi on in power save mode. Go to settings.
