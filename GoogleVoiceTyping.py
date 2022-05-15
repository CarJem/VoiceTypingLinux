# ---- Google Voice Typing with Python ----
# [    Designed for Valve's Steam Deck    ]

# Co Programmer / Inital Idea: 
# - Carter "CarJem" Wallace
#   https://github.com/carjem

# Co Programmer: 
# - Anguel Esperanza
#   https://github.com/anguelesperanza

import json
import os
from subprocess import call
import subprocess
import time
import signal 
import speech_recognition as sr

rec_process = None
send_filename = 'SEND'
lock_filename = 'LOCK'
wait_filename = 'WAIT'
wav_filename = 'file.wav'

def getAssetFolder():
    try:
        f = open('config.json')
        data = json.loads(f.read())
        return data['soundFolder']
    except:
        return 'assets'

def setLock(state):
    if state:
        with open(lock_filename, 'w') as f:
            f.write('')
    else:
        os.remove(lock_filename)

def setSend(state):
    if state:
        with open(send_filename, 'w') as f:
            f.write('')
    else:
        os.remove(send_filename)

def canSend():
    file_names = os.listdir()
    if send_filename in file_names:
        return True
    else: 
        return False

def idleWhileRecording():
    oldepoch = time.time()
    pendingRecordStop = False
    while pendingRecordStop == False:
        result = canSend()
        if result: 
            pendingRecordStop = True
        if time.time() - oldepoch >= 30: 
            setSend(True)

def startRecording():
    global rec_process
    setLock(True)
    cmd = 'arecord -q -t wav -f S32_LE ' + wav_filename
    rec_process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    play_sound('start')

def endRecording():
    global rec_process
    rec_process.send_signal(signal.SIGINT)
    rec_process.wait()
    rec_process = None
    play_sound('end')

def speechToText():
    r = sr.Recognizer()

    with sr.AudioFile(wav_filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        os.popen('xdotool type "{0}"'.format(text))

def clear_cache(failed):
    if failed == True:
        play_sound('fail')

    files = os.listdir()
    
    if send_filename in files: 
        os.remove(send_filename)
    if wait_filename in files: 
        os.remove(wait_filename)
    if wav_filename in files: 
        os.remove(wav_filename)
    if lock_filename in files: 
        os.remove(lock_filename)
    if rec_process != None: 
        rec_process.kill()


def play_sound(type):
    asset_folder = getAssetFolder()
    try:
        sound_file = "{0}/{1}.wav".format(asset_folder, type)
        call(["aplay", "-q", sound_file])
    except Exception as ex:
        print(ex)
        print('Something went wrong when trying to play: {0}/{1}.wav'.format(asset_folder, type))

def main():
    try:
        startRecording()
        idleWhileRecording()
        endRecording()
        speechToText()
        clear_cache(False)
    except Exception as ex:
        print(ex)
        clear_cache(True)

if __name__=='__main__':
    main()