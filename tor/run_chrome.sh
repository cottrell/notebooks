#!/bin/bash
# https://askubuntu.com/questions/35392/how-to-launch-a-new-instance-of-google-chrome-from-the-command-line
google-chrome --proxy-server="socks5://127.0.0.1:9050" --user-data-dir=$(mktemp -d)

