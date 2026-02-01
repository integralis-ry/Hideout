#!/bin/bash
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver x11-xserver-utils wireless-tools python3-pip python3-venv
cd /home/integralis/Hideout/display
python3 -m venv venv
./venv/bin/pip install -r requirements.txt