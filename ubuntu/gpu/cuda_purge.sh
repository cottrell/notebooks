#!/bin/sh -e
sudo apt-get purge '*cuda*' -y
sudo apt-get purge '*cudnn*' -y
sudo apt-get autoremove -y
sudo apt list --installed | grep cud
