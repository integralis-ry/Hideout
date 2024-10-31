#!/usr/bin/bash

git pull

# Run the Python script and always execute the following commands, but
# check success to determine which set of commands to run after.
python3 unicafe_web_scarper/app.py

# Commands that should run regardless of success or failure of app.py
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

# Check if app.py was successful, and if so, run additional commands
if [ $? -eq 0 ]; then
    echo "app.py executed successfully. Running additional commands..."
    python3 display.py
else
    echo "app.py failed, skipping additional success-only commands."
fi
