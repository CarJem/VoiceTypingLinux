import os
from google.cloud import speech
import subprocess
import time
import signal 

#Lead Programmer: Carter "CarJem" Wallace; https://github.com/carjem
#Co Programmer: Anguel Esperanza; https://github.com/anguelesperanza

rec_process = None
lock_filename = 'LOCK'
wait_filename = 'WAIT'
flac_filename = 'file.flac'
wav_filename = 'file.wav'

def update_lock(state):
    if state:
        with open(lock_filename, 'w') as f:
            f.write()
    else:
        os.remove(lock_filename)

def have_lock():
    file_names = os.listdir()
    if lock_filename in file_names:
        return True
    else: return False

def record_wait():
    i = 0
    pendingRecordStop = False
    while pendingRecordStop == False:
        result = have_lock()
        if result: pendingRecordStop = True
        i += 1
        time.sleep(1)
        if i >= 30: update_lock(True)

def start_record():
    global rec_process
    cmd = 'arecord -q -t wav -f S32_LE ' + wav_filename
    rec_process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

def end_record():
    update_lock(False)
    global rec_process
    rec_process.send_signal(signal.SIGINT)
    rec_process.wait()
    rec_process = None
    cmd = 'ffmpeg -hide_banner -loglevel error -i file.wav -y ' + flac_filename + ' -ar 16000'
    convert_process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    convert_process.wait()

def stt_test():
    result_string = "CarJem was Here"
    os.popen('xdotool type "{0}"'.format(result_string))

def stt():
    result_string = ""
    client = speech.SpeechClient.from_service_account_file('key.json')

    with open(flac_filename, 'rb') as f:
        flac_data = f.read()

    audio_file = speech.RecognitionAudio(content=flac_data)

    config = speech.RecognitionConfig(
        sample_rate_hertz=8000,
        enable_automatic_punctuation=True,
        language_code='en-US'
    )

    response = client.recognize(
        config=config,
        audio=audio_file
    )

    for result in response.results:
        #print(result)
        result_string = result.alternatives[0].transcript

    os.popen('xdotool type "{0}"'.format(result_string))

def clear_cache():
    files = os.listdir()
    if lock_filename in files: os.remove(lock_filename)
    if wait_filename in files: os.remove(wait_filename)
    if flac_filename in files: os.remove(flac_filename)
    if wav_filename in files: os.remove(wav_filename)
    if rec_process != None: rec_process.kill()

def main():
    try:
        start_record()
        record_wait()
        end_record()
        stt()
        clear_cache()
    except:
        clear_cache()


    

if __name__=='__main__':
    main()