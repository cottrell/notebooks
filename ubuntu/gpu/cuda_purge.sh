#!/bin/sh -e
sudo apt-get autoremove --purge cuda
sudo apt purge '*cuda*'
sudo apt autoremove
sudo apt update
