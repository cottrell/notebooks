#!/bin/sh
RELEASE=impish
VERSION=21.10
wget http://releases.ubuntu.com/$RELEASE/ubuntu-$VERSION-desktop-amd64.manifest -q -O - | cut -f 1 | xargs | tr ' ' '\n'
