#!/bin/bash


./uninstall_service_a.sh
sudo -S ./uninstall_service_b.sh

pyinstaller GoogleVoiceTyping.py
cp ./toggle.sh ./dist/GoogleVoiceTyping/toggle.sh
cp ./config.json ./dist/GoogleVoiceTyping/config.json
cp -r ./assets ./dist/GoogleVoiceTyping/assets/
cp -r ./assets_google ./dist/GoogleVoiceTyping/assets_google/


cd _service ; pyinstaller --onefile service.py ; cd ..
cp ./_service/dist/service ./dist/GoogleVoiceTyping/service 


./install_service_a.sh
sudo -S ./install_service_b.sh
