import os
import subprocess
import time
import keyboard

def run_script():
    with open(os.open('REQUEST', os.O_CREAT | os.O_WRONLY, 0o777), 'w') as f:
        f.write('')


keyboard.add_hotkey("win+ctrl+g", run_script)

while True:
    time.sleep(1)