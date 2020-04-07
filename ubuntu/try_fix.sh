[[ -e rtl8188eu ]] || git clone https://github.com/lwfinger/rtl8188eu.git
cd rtl8188eu
make all
sudo make install
echo sudo systemctl reboot
