#!/bin/bash -e
sudo killall -HUP mDNSResponder;
sudo dscacheutil -flushcache
