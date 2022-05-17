# ----    Voice Typing with Python     ----
# [    Designed for Valve's Steam Deck    ]

# Co Programmer / Inital Idea: 
# - Carter "CarJem" Wallace
#   https://github.com/carjem

# Co Programmer: 
# - Anguel Esperanza
#   https://github.com/anguelesperanza

import json
import os
from pickle import NONE
import subprocess
import sys
import time
import signal 
import azure.cognitiveservices.speech as speechsdk

rec_process = None

SEND_COMMAND = 'SEND'
LOCK_COMMAND = 'LOCK'
RESULT_COMMAND = 'RESULT'
WAIT_COMMAND = 'WAIT'
REQUEST_COMMAND = 'REQUEST'

wav_filename = 'file.wav'
config_filename = 'config.json'

wait_time = 15


#region Typing Validation

def typingGetResult(srr: str = None) -> bool:
    typingOutput = None
    if srr == None:
        typingOutput = subprocess.check_output(['/usr/bin/xdotool type ""'], shell=True, universal_newlines=True)
    else:
        typingOutput = subprocess.check_output(['/usr/bin/xdotool type \"{}\"'.format(srr)], shell=True, universal_newlines=True)

    if "Failed creating new xdo instance" in typingOutput:
        return False
    else:
        return True

#endregion

#region Various Actions

def getConfigEntry(key, defaultValue = None):
    try:
        f = open(config_filename)
        data = json.loads(f.read())
        return data[key]
    except:
        return defaultValue

def clearCache(error):
    if error == True:
        playSound('error')
 
    setCommand(SEND_COMMAND, False)
    setCommand(WAIT_COMMAND, False)
    setCommand(LOCK_COMMAND, False)
    setCommand(SEND_COMMAND, False)

    files = os.listdir()

    if wav_filename in files: 
        os.remove(wav_filename)

    if rec_process != None: 
        rec_process.kill()

def playSound(type):
    asset_folder = getConfigEntry('soundFolder', 'assets')
    try:
        sound_file = "{0}/{1}.wav".format(asset_folder, type)
        subprocess.call(["aplay", "-q", sound_file])
    except Exception as ex:
        print(ex)
        print('Something went wrong when trying to play: {0}/{1}.wav'.format(asset_folder, type))

#endregion

#region Command Set/Get

def setCommand(command, state):
    if state:
        with open(command, 'w') as f:
            f.write('')
    else:
        files = os.listdir()
        if command in files: 
            os.remove(command)

def hasCommand(command):
    file_names = os.listdir()
    if command in file_names:
        return True
    else: 
        return False

#endregion

#region Recording

def recordingIdle():
    oldepoch = time.time()
    pendingRecordStop = False
    while pendingRecordStop == False:
        result = hasCommand(SEND_COMMAND)
        if result: 
            pendingRecordStop = True
        if time.time() - oldepoch >= wait_time: 
            setCommand(SEND_COMMAND, True)

def recordingStart():
    global rec_process
    setCommand(LOCK_COMMAND, True)
    cmd = 'arecord -q -t wav -f S32_LE ' + wav_filename
    rec_process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    playSound('start')

def recordingEnd():
    global rec_process
    rec_process.send_signal(signal.SIGINT)
    rec_process.wait()
    rec_process = None
    playSound('end')

#endregion

#region Speech

def speechTextToKeyboard(srr) -> bool:
    wasTypingSuccessful = typingGetResult(srr.text)
    #wasTypingSuccessful = typingGetResult("Testing")

    if srr.reason == speechsdk.ResultReason.NoMatch:
        playSound('fail')
        print("No speech could be recognized: {}".format(srr.no_match_details))

    elif srr.reason == speechsdk.ResultReason.Canceled:
        playSound('fail')
        cancelInfo = srr.cancellation_details
        print("Speech Recognition canceled: {}".format(cancelInfo.reason))

        if cancelInfo.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancelInfo.error_details))
            print("Did you set the speech resource key and region values?")

    return wasTypingSuccessful

def speechToText() -> bool:
    speech_key = getConfigEntry('azure_key', None)
    service_region = getConfigEntry('azure_region', None)
    service_lang = getConfigEntry('azure_lang', "en-US")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=wav_filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language=service_lang, audio_config=audio_config)
    srr = speech_recognizer.recognize_once()
    return speechTextToKeyboard(srr)

#endregion

#region Service

def serviceRun():
    try:
        recordingStart()
        recordingIdle()
        recordingEnd()
        typingSuccessful = speechToText()
        clearCache(False)
        if not typingSuccessful:
            serviceRestart()
    except Exception as ex:
        print(ex)
        clearCache(True)

def serviceRestart():
    print("Restarting Voice Typing Service...")
    playSound('restart')
    setCommand(LOCK_COMMAND, True)
    subprocess.Popen(["systemctl --user disable voicetyping-core.service"])
    time.sleep(5)
    subprocess.Popen(["systemctl --user enable voicetyping-core.service"])
    setCommand(LOCK_COMMAND, False)
    playSound('startup')


def serviceGetExecutable() -> str:
    if "--DEBUG" in sys.argv:
        return 'python ./voice-typing.py'
    else:
        return './voice-typing'

def serviceLoop():
    keepRunning = True
    while keepRunning:
        file_names = os.listdir()
        if REQUEST_COMMAND in file_names:
            setCommand(REQUEST_COMMAND, False)
            if WAIT_COMMAND in file_names:
                setCommand(WAIT_COMMAND, False)
                setCommand(SEND_COMMAND, True)
            elif LOCK_COMMAND in file_names:
                print("Can't run multiple instances")
            else:
                if typingGetResult():
                    subprocess.Popen([serviceGetExecutable()], shell=True)
                    setCommand(WAIT_COMMAND, True)
                else:
                    keepRunning = False
                    clearCache(False)
                    serviceRestart()

        time.sleep(1)

def main():
    if '--SERVICE' in sys.argv:
        serviceLoop()
    else:
        serviceRun()

#endregion

if __name__=='__main__':
    main()