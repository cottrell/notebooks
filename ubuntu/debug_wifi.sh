#!/bin/sh
# iwconfig
# sudo ifconfig enx503eaa4de20b down
# sudo iwconfig enx503eaa4de20b power off
# sudo ifconfig enx503eaa4de20b up
# sudo service network-manager restart
# lshw -C network
# dmesg | grep -e enx -e rtl
# cat syslog | grep -e enx -e rtl
cat syslog | grep -e enx -e rtl | less
