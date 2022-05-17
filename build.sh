#!/bin/bash
cd "$(dirname "$0")" || return

# Uninstall Old Services
./services/scripts/service-core-uninstall.sh
./services/scripts/service-reloader-uninstall.sh
sudo -S ./services/scripts/service-listener-uninstall.sh

# Build Voice-Typing
pyinstaller -y --console voice-typing.py

# Copy Build Output Files
# cp ./voice-typing-toggle.sh ./dist/voice-typing/voice-typing-toggle.sh
#cp ./voice-typing-reload-service.sh ./dist/voice-typing/voice-typing-reload-service.sh
cp -r ./assets ./dist/voice-typing/assets/

if [ -f 'config.dev.json' ]; then
    cp ./config.dev.json ./dist/voice-typing/config.json
else
    cp ./config.json ./dist/voice-typing/config.json
fi

# Build Voice-Typing-Listener-Service
cd services || return 
pyinstaller -y --onefile voice-typing-listener-service.py
cd ..
echo "$PWD"

cp ./services/dist/voice-typing-listener-service ./dist/voice-typing/voice-typing-listener-service 

# Install Services
./services/scripts/service-core-install.sh
#./services/scripts/service-reloader-install.sh
sudo -S ./services/scripts/service-listener-install.sh
