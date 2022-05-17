from asyncore import read
import json
import os
import subprocess
import time
from turtle import delay
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

def type_result():
    try:
        file_names = os.listdir()
        if 'RESULT' in file_names:
            with open('RESULT', 'r') as f:
                result = f.read()
            keyboard.write(result, delay=0.05, exact=False)
            os.remove('RESULT')
    except Exception as e:
        print(repr(e))
        pass


keyboard.add_hotkey(getKeybind(), run_script)

while True:
    type_result()
    time.sleep(1)