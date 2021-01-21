
MacOS:
    sudo killall -HUP mDNSResponder

dns-sd -q bleepblop

dscacheutil -q host -a name bleepblop
