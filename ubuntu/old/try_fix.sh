# nope
# [[ -e rtl8188eu ]] || git clone https://github.com/lwfinger/rtl8188eu.git
# cd rtl8188eu
# make all
# sudo make install
# echo sudo systemctl reboot

# https://askubuntu.com/questions/1224074/no-wifi-adapter-found-in-gnome-control-center/1225019#1225019
git clone https://github.com/gnab/rtl8812au.git
cd rtl8812au
sudo rsync -rvhP ./ /usr/src/8812au-4.2.2
sudo dkms add -m 8812au -v 4.2.2
sudo dkms build -m 8812au -v 4.2.2
sudo dkms install -m 8812au -v 4.2.2
sudo modprobe 8812au
