import json
import os
import subprocess
import time
import keyboard


def getKeybind():
    try:
        f = open('config.json')
        data = json.loads(f.read())
        return data['keybind']
    except:
        return 'win+ctrl+z'

def run_script():
    with open(os.open('REQUEST', os.O_CREAT | os.O_WRONLY, 0o777), 'w') as f:
        f.write('')


keyboard.add_hotkey(getKeybind(), run_script)

while True:
    time.sleep(1)