import os, time, json, subprocess

with open("config.json") as f:
    config = json.load(f)

# Start Chromium with the first URL
first_url = config["urls"][0]["url"]
proc = subprocess.Popen(["chromium-browser", "--kiosk", first_url])
time.sleep(5)  # Wait for Chromium to launch

while True:
    for entry in config["urls"]:
        url, duration = entry["url"], entry["duration"]
        # Focus address bar, type URL, press Enter
        subprocess.run(["xdotool", "key", "ctrl+l"])
        subprocess.run(["xdotool", "type", url])
        subprocess.run(["xdotool", "key", "Return"])
        time.sleep(duration)