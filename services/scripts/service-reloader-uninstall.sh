#!/bin/bash
systemctl --user stop voicetyping-reloader 2> /dev/null
systemctl --user disable voicetyping-reloader 2> /dev/null
rm -f /home/deck/.config/systemd/user/voicetyping-reloader.service
