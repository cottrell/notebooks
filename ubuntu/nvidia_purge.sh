#!/bin/sh -e

# shoot me

# generally you don't want to just run this, it times out and you don't need to repurge all the time
sudo apt purge ^nvidia
# sudo apt autoremove
# sudo add-apt-repository --remove ppa:graphics-drivers/ppa
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
# sudo apt install nvidia-driver-396
sudo ubuntu-drivers autoinstall
echo check nvidia-smi after reboot
echo now reboot
