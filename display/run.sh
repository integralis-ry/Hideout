#!/usr/bin/bash

cp info.html info_configured.html

SSID=$(iwgetid -r)
IP=$(hostname -I)
WHOAMI=$(whoami)
GITHUB='https://github.com/integralis-ry/Hideout'
ESCAPED_GITHUB=$(printf '%s\n' "$GITHUB" | sed -e 's/[\/&]/\\&/g')
EMAIL='it@integralis.fi'

sed -i -e "s/{{SSID}}/$SSID/g" info_configured.html
sed -i -e "s/{{IP}}/$IP/g" info_configured.html
sed -i -e "s/{{WHOAMI}}/$WHOAMI/g" info_configured.html
sed -i -e "s/{{GITHUB}}/$ESCAPED_GITHUB/g" info_configured.html
sed -i -e "s/{{EMAIL}}/$EMAIL/g" info_configured.html

python3 display.py
