#!/bin/bash

pyinstaller GoogleVoiceTyping.py
cp ./toggle.sh ./dist/GoogleVoiceTyping/toggle.sh
cp ./config.json ./dist/GoogleVoiceTyping/config.json
cp -r ./assets ./dist/GoogleVoiceTyping/assets/
cp -r ./assets_google ./dist/GoogleVoiceTyping/assets_google/


cd _service ; pyinstaller --onefile service.py ; cd ..
cp ./_service/dist/service ./dist/GoogleVoiceTyping/service 

