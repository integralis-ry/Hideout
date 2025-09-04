import os, time, json, subprocess

with open("config_configured.json") as f:
    config = json.load(f)

while True:
    for entry in config["urls"]:
        url, duration = entry["url"], entry["duration"]
        proc = subprocess.Popen(["chromium-browser", "--kiosk", url])
        time.sleep(duration)
        proc.terminate()
