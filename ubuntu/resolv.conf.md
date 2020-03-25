https://www.hiroom2.com/2017/08/24/ubuntu-1610-nameserver-127-0-0-53-en/
https://askubuntu.com/questions/1012641/dns-set-to-systemds-127-0-0-53-how-to-change-permanently

Adding nameserver 192.168.1.1 to /etc/resolv.conf is necessary. Not sure will survive reboot.


Finally did this, this is an unbelievable amount of noise on this. No idea what they are doing.

    $ cat /etc/network/interfaces
    # interfaces(5) file used by ifup(8) and ifdown(8)
    auto lo
    iface lo inet loopback
    	dns-nameservers 192.168.1.1


This was the old file:
--- /etc/systemd/resolved.conf	2018-12-22 13:47:25.240352187 +0000
+++ /etc/systemd/resolved.conf.dpkg-new	2020-02-06 14:45:57.000000000 +0000
@@ -12,12 +12,13 @@
 # See resolved.conf(5) for details

 [Resolve]
-DNS=8.8.8.8
-DNS=8.8.4.4
+#DNS=
 #FallbackDNS=
 #Domains=
 #LLMNR=no
 #MulticastDNS=no
 #DNSSEC=no
+#DNSOverTLS=no
 #Cache=yes
 #DNSStubListener=yes
+#ReadEtcHosts=yes

