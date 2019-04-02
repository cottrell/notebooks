#!/bin/sh -e

# (36) cottrell@bleepblop:~$ nvidia-smi
# Sat Mar 23 16:43:33 2019       
# +-----------------------------------------------------------------------------+
# | NVIDIA-SMI 410.104      Driver Version: 410.104      CUDA Version: 10.0     |
# |-------------------------------+----------------------+----------------------+
# | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
# | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
# |===============================+======================+======================|
# |   0  GeForce RTX 2070    Off  | 00000000:01:00.0  On |                  N/A |
# | 30%   36C    P0    44W / 175W |    279MiB /  7949MiB |      1%      Default |
# +-------------------------------+----------------------+----------------------+
#                                                                                
# +-----------------------------------------------------------------------------+
# | Processes:                                                       GPU Memory |
# |  GPU       PID   Type   Process name                             Usage      |
# |=============================================================================|
# |    0      1609      G   /usr/lib/xorg/Xorg                            18MiB |
# |    0      1682      G   /usr/bin/gnome-shell                          50MiB |
# |    0      2531      G   /usr/lib/xorg/Xorg                            90MiB |
# |    0      2665      G   /usr/bin/gnome-shell                         117MiB |
# +-----------------------------------------------------------------------------+


# NOT SURE NOT SURE MAYBE ONLY cuda 10.0 supported and nvidia driver 410?

sudo apt purge ^nvidia
sudo apt purge '*cuda*'
sudo apt autoremove
sudo add-apt-repository --remove ppa:graphics-drivers/ppa
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo apt install nvidia-driver-410

# shoot me

# # generally you don't want to just run this, it times out and you don't need to repurge all the time
# sudo apt purge ^nvidia
# sudo apt purge '*cuda*'
# sudo apt autoremove
# sudo add-apt-repository --remove ppa:graphics-drivers/ppa
# sudo add-apt-repository ppa:graphics-drivers/ppa
# sudo apt update
# # sudo apt install nvidia-driver-396
# # sudo ubuntu-drivers autoinstall
# echo check nvidia-smi after reboot
# echo now reboot
