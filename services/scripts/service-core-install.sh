#!/bin/bash
cd "$(dirname "$0")"

./service-core-uninstall.sh
cat > /home/deck/.config/systemd/user/voicetyping-core.service <<- EOM
[Unit]
Description=Voice Typing - Core Service

[Service]
Type=simple
Group=deck
Restart=always
# ExecStartPre=/bin/sleep 10
ExecStart=/home/deck/homebrew/other_services/voice-typing/voice-typing --SERVICE
WorkingDirectory=/home/deck/homebrew/other_services/voice-typing

[Install]
WantedBy=default.target
EOM
systemctl --user daemon-reload
systemctl --user start voicetyping-core
systemctl --user enable voicetyping-core
