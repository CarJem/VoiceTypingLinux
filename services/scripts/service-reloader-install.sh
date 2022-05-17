#!/bin/bash
cd "$(dirname "$0")"

./service-reloader-uninstall.sh
cat > /home/deck/.config/systemd/user/voicetyping-reloader.service <<- EOM
[Unit]
Description=Voice Typing - Reload Service

[Service]
Type=simple
Group=deck
Restart=always
ExecStart=/home/deck/homebrew/other_services/voice-typing/voice-typing-reload-service.sh
WorkingDirectory=/home/deck/homebrew/other_services/voice-typing

[Install]
WantedBy=default.target
EOM
systemctl --user daemon-reload
systemctl --user start voicetyping-reloader
systemctl --user enable voicetyping-reloader
