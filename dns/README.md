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

# slow DNS?

https://www.math.tamu.edu/~comech/tools/linux-slow-dns-lookup/

See ubuntu/resolve.conf.md

Very slow:

```shell
$ make test
dig +trace www.stackoverflow.com

; <<>> DiG 9.16.15-Ubuntu <<>> +trace www.stackoverflow.com
;; global options: +cmd
;; connection timed out; no servers could be reached

make: *** [Makefile:8: test] Error 9


$ make view
systemd-resolve --status
Global
       Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
resolv.conf mode: uplink

Link 2 (enp3s0)
Current Scopes: none
     Protocols: -DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported

Link 3 (wlxa09f10b9ff56)
    Current Scopes: DNS
         Protocols: +DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 10.0.0.1
       DNS Servers: 10.0.0.1

Link 4 (docker0)
Current Scopes: none
     Protocols: -DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
```

Trying `make clear` ... no improvement.

Adding Google entry in `/etc/systemd/resolved.conf` ... `DNS=8.8.8.8` etc then `make restart` ... still no update in /etc/resolv.conf.

See `nmcli` ...

Still nothing working. Trying a restart.

Is good after restart. Not sure what triggers the rebuilt. `make test` is fast.

```shell
$ make view
systemd-resolve --status
Global
       Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
resolv.conf mode: uplink
     DNS Servers: 8.8.8.8 8.8.4.4

Link 2 (enp3s0)
Current Scopes: none
     Protocols: -DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported

Link 3 (wlxa09f10b9ff56)
    Current Scopes: DNS
         Protocols: +DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 10.0.0.1
       DNS Servers: 10.0.0.1

Link 4 (docker0)
Current Scopes: none
     Protocols: -DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
```
