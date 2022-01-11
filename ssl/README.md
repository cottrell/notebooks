# debug 2022-01-02 of ssl.com

Summary: antique macs appear to be the issue. They have root stores that go
stale. You need to copy one over and run some script. See the last two things
at the end of this section.

Do this to test:

    openssl s_client -connect apt.syncthing.net:443

For example if a site (example ssl.com) is showing as cert not trusted)

debug in chrome, see the security stuff and download the cert.

Try ssllabs.com tool first.

Clear other caches (DNS)

https://www.wpbeginner.com/wp-tutorials/how-to-clear-your-dns-cache-mac-windows-chrome/

chrome://net-internals/#dns

Sounding like device root stores are stale?

* (read this) https://www.thesslstore.com/blog/root-certificates-intermediate/
* (do this) https://apple.stackexchange.com/questions/422332/how-do-i-update-my-root-certificates-on-an-older-version-of-mac-os-e-g-el-capi


# debug of 2022-01-11 syncthing ssl cert error

    openssl s_client -connect apt.syncthing.net:443  # here you see the CA X3 cert and google it
    openssl x509 -enddate -noout -in /etc/ssl/certs/DST_Root_CA_X3.pem  # see the expiry
    # ok just remove it
    sudo rm /etc/ssl/certs/DST_Root_CA_X3.pem
    sudo update-ca-certificates # ... needed this I think
    sudo apt-get update

