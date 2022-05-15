#!/bin/bash

# SERVICE B
./uninstall_service_b.sh
cat > /etc/systemd/system/google_voice_typing_b.service <<- EOM
[Unit]
Description=Google Voice Typing Service (B)

[Service]
Type=simple
User=root
Restart=always
ExecStart=/home/deck/homebrew/other_services/google_voice_typing/service
WorkingDirectory=/home/deck/homebrew/other_services/google_voice_typing

[Install]
WantedBy=multi-user.target
EOM
systemctl daemon-reload
systemctl start google_voice_typing_b
systemctl enable google_voice_typing_b