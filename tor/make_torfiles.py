#!/usr/bin/env python
import argh

TXT = """\
SocksPort {socks_port}
ControlPort {control_port}
CookieAuthentication 1
DataDirectoryGroupReadable 1
CookieAuthFileGroupReadable 1
ExtORPortCookieAuthFileGroupReadable 1
CacheDirectoryGroupReadable 1
DataDirectory /var/lib/tor_{i}
"""

BASE_PORT = 9050

TORRC = '/etc/tor/torrc.{i}'


def make_files(n=5):
    for i in range(n):
        socks_port = BASE_PORT + 2 * i
        control_port = BASE_PORT + 2 * i + 1
        txt = TXT.format(socks_port=socks_port, control_port=control_port, i=i)
        filename = TORRC.format(i=i)
        print(f'writing to {filename}:\n\n{txt}')
        with open(filename, 'w') as fout:
            fout.write(txt)


if __name__ == '__main__':
    argh.dispatch_command(make_files)
