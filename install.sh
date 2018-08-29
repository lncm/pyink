#!/usr/bin/env bash

apt-get update
apt-get upgrade -y
apt-get install python-pip python-dev python-smbus python-serial libjpeg9-dev -y

python -m pip install --upgrade pip
python -m pip install pillow
python -m pip install qrcode
python -m pip install spidev

# Make sure i2c-dev is above i2c-bcm2708
echo 'i2c-dev' >> /etc/modules
echo 'i2c-bcm2708' >> /etc/modules

echo -e "\nRequired by Satoshi-Pay" >> /boot/config.txt
echo "dtparam=i2c_arm=on" >> /boot/config.txt
echo "dtparam=spi=on" >> /boot/config.txt

echo -e '\nWARNING! Please make sure to save all open files.\n'

echo "Do you wish reboot now?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) 'reboot'; break;;
        No ) echo -e "\nYou need to reboot before the software can be used."; exit;;
    esac
done