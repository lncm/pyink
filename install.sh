#!/usr/bin/env bash

# Abort on any non-zero exit status
set -e

doInstall() {
    apt-get update
    apt-get upgrade -y
    apt-get install git python-pip python-dev python-smbus python-serial libjpeg9-dev -y

    python -m pip install --upgrade pip
    python -m pip install pillow
    python -m pip install qrcode
    python -m pip install spidev

    git clone https://github.com/lncm/Satoshi-Pi.git
    chmod +x Satoshi-Pi/run.sh

    # Make sure i2c-dev is above i2c-bcm2708
    echo 'i2c-dev' >> /etc/modules
    echo 'i2c-bcm2708' >> /etc/modules

    echo -e "\nRequired by Satoshi-Pi" >> /boot/config.txt
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
}

# User is root if user ID is 0
if [[ "${EUID}" -eq 0 ]]; then
    doInstall
else
    echo "This installer must be run with sudo or as root"
    # Check if sudo command exists
        if command -v sudo &> /dev/null; then
            echo "Attempting to run with sudo"
            exec sudo bash curl -sS https://raw.githubusercontent.com/lncm/Satoshi-Pi/master/install.sh
        else
            echo "Cannot find sudo"
        fi
fi



