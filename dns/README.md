# DNS debug


    iwconfig # look for device

    nmcli device show <devicename>

And you change the dns hosts through the settings -> wifi -> options cog -> ipv4 etc

Check things with this:

    systemd-resolve --status

    dig +trace www.google.co.uk


Also run:

    sudo tcpdump


and the try ping in another terminal to see what happens.
