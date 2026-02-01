#!/usr/bin/bash

# force last version of repo to be the github one
git reset --hard origin/main

DIR=$(pwd)
VENV_PYTHON="$DIR/venv/bin/python3"
MENU_DIR="/home/integralis/Hideout/unicafe_menu_creation"

pkill -f python3
sleep 1

cd "$DIR"
git reset --hard origin/main
cp info.html info_configured.html
cp config.json config_configured.json

SSID=$(iwgetid -r)
IP=$(hostname -I)
WHOAMI=$(whoami)
GITHUB='https://github.com/integralis-ry/Hideout'
GITHUB_ESC=$(printf '%s\n' "$GITHUB" | sed -e 's/[\/&]/\\&/g')
EMAIL='it@integralis.fi'
DIR_ESC=$(printf '%s\n' "$DIR" | sed -e 's/[\/&]/\\&/g')

sed -i -e "s/{{SSID}}/$SSID/g" info_configured.html
sed -i -e "s/{{IP}}/$IP/g" info_configured.html
sed -i -e "s/{{WHOAMI}}/$WHOAMI/g" info_configured.html
sed -i -e "s/{{GITHUB}}/$GITHUB_ESC/g" info_configured.html
sed -i -e "s/{{EMAIL}}/$EMAIL/g" info_configured.html
sed -i -e "s/{{DIR}}/$DIR_ESC/g" config_configured.json

export DISPLAY=:0

echo "Running Menu Finder..."
$VENV_PYTHON "$MENU_DIR/menu_finder.py"
sleep 5

echo "Starting Menu Creation App in background..."
$VENV_PYTHON "$MENU_DIR/app.py" & 
sleep 2

echo "Launching Kiosk Display..."
$VENV_PYTHON "$DIR/display.py"
