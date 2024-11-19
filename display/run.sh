#!/usr/bin/bash

# Update the codebase
git pull

# Get the Raspberry Pi's local IP address
IP_ADDRESS=$(hostname -I | awk '{print $1}')
WEB_URL="http://$IP_ADDRESS:5000"

# Start the Flask app in the background
python3 board_dir/app.py &

# Wait a few seconds to ensure Flask is running
sleep 15

# Launch the leaderboard in kiosk mode on Firefox
firefox --kiosk "$WEB_URL"
