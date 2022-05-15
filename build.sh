#!/bin/bash

pyinstaller GoogleVoiceTypingPY.py
cp ToggleVoiceTyping.sh dist/GoogleVoiceTypingPY/ToggleVoiceTyping.sh
cp -r ./assets ./dist/GoogleVoiceTypingPY/assets/


cd _service
pyinstaller --onefile service.py
cd ..

cp _service/dist/service dist/GoogleVoiceTypingPY/service 

