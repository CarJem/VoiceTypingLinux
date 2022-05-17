#!/bin/bash
cd "$(dirname "$0")" || return

# Uninstall Old Services
./services/scripts/service-core-uninstall.sh
sudo -S ./services/scripts/service-listener-uninstall.sh

# Build Voice-Typing
pyinstaller -y --console voice-typing.py

# Copy Build Output Files
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
sudo -S ./services/scripts/service-listener-install.sh
