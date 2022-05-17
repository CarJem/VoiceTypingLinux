#!/bin/bash
cd "$(dirname "$0")"

./service-listener-uninstall.sh
cat > /etc/systemd/system/voicetyping-listener.service <<- EOM
[Unit]
Description=Voice Typing - Hotkey Service

[Service]
Type=simple
User=root
Restart=always
# ExecStartPre=/bin/sleep 10
ExecStart=/home/deck/homebrew/other_services/voice-typing/voice-typing-listener-service
WorkingDirectory=/home/deck/homebrew/other_services/voice-typing

[Install]
WantedBy=multi-user.target
EOM
systemctl daemon-reload
systemctl start voicetyping-listener
systemctl enable voicetyping-listener