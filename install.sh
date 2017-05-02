#!/usr/bin/env bash

# Install Python (python 2.7 & 3.x)
[[ -z $(which python) ]] && sudo apt-get --yes --force-yes install python
[[ -z $(which python2.7) ]] && sudo apt-get --yes --force-yes install python2.7
[[ -z $(which python3) ]] && sudo apt-get --yes --force-yes install python3

# Install pip
[[ -z $(which python-pip) ]] && sudo apt-get --yes --force-yes install python-pip
[[ -z $(which python3-pip) ]] && sudo apt-get --yes --force-yes install python3-pip

# Install & Upgrade Raspberry Pi GPIO python library
[[ -z $(which python-rpi.gpio) ]] && sudo apt-get --yes --force-yes install python-rpi.gpio
[[ -z $(which python3-rpi.gpio) ]] && sudo apt-get --yes --force-yes install python3-rpi.gpio
sudo pip2 install --upgrade RPi.GPIO
sudo pip3 install --upgrade RPi.GPIO

# Copy latest version of gpio read-write python script
wget -P script/ https://raw.githubusercontent.com/QuentinCG/Base-Scripts/master/Raspberry_Pi/utils/readWriteGpio.py
