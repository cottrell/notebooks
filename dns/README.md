# DNS debug


    iwconfig # look for device

    nmcli device show <devicename>

And you change the dns hosts through the settings -> wifi -> options cog -> ipv4 etc

Check things with this:

    systemd-resolve --status

    dig +trace www.google.co.uk
