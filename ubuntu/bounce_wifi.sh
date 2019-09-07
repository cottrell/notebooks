#!/bin/sh
# iwconfig
# sudo ifconfig enx503eaa4de20b down
# sudo iwconfig enx503eaa4de20b power off
# sudo ifconfig enx503eaa4de20b up
# sudo service network-manager restart
# lshw -C network
# dmesg | grep -e enx -e rtl
# cat syslog | grep -e enx -e rtl
# tail -f /var/log/syslog
# | grep -e enx -e rtl | less

# sudo sysmtemctl restart NetworkManager
nmcli radio wifi off && sleep 5 && nmcli radio wifi on
