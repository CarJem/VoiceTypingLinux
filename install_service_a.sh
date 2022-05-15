#!/bin/bash

# SERVICE A
systemctl --user stop google_voice_typing_a 2> /dev/null
systemctl --user disable google_voice_typing_a 2> /dev/null
rm -f /home/deck/.config/systemd/user/google_voice_typing_a.service
cat > /home/deck/.config/systemd/user/google_voice_typing_a.service <<- EOM
[Unit]
Description=Google Voice Typing Service (A)

[Service]
Type=simple
Restart=always
ExecStart=/home/deck/homebrew/other_services/google_voice_typing/toggle.sh --SERVICE
WorkingDirectory=/home/deck/homebrew/other_services/google_voice_typing

[Install]
WantedBy=default.target
EOM
systemctl --user daemon-reload
systemctl --user start google_voice_typing_a
systemctl --user enable google_voice_typing_a
