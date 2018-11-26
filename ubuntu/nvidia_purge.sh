#!/bin/sh -e

# shoot me

sudo apt purge ^nvidia
sudo apt autoremove
sudo add-apt-repository --remove ppa:graphics-drivers/ppa
sudo apt update
sudo ubuntu-drivers autoinstall
echo check nvidia-smi after reboot
sudo reboot


