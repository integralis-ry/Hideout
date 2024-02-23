#!/usr/bin/bash

cp info.html info_configured.html
cp config.json config_configured.json

SSID=$(iwgetid -r)
IP=$(hostname -I)
WHOAMI=$(whoami)
GITHUB='https://github.com/integralis-ry/Hideout'
GITHUB_ESC=$(printf '%s\n' "$GITHUB" | sed -e 's/[\/&]/\\&/g')
EMAIL='it@integralis.fi'
DIR=$(pwd)
DIR_ESC=$(printf '%s\n' "$DIR" | sed -e 's/[\/&]/\\&/g')


sed -i -e "s/{{SSID}}/$SSID/g" info_configured.html
sed -i -e "s/{{IP}}/$IP/g" info_configured.html
sed -i -e "s/{{WHOAMI}}/$WHOAMI/g" info_configured.html
sed -i -e "s/{{GITHUB}}/$GITHUB_ESC/g" info_configured.html
sed -i -e "s/{{EMAIL}}/$EMAIL/g" info_configured.html
sed -i -e "s/{{DIR}}/$DIR_ESC/g" config_configured.json

python3 display.py
