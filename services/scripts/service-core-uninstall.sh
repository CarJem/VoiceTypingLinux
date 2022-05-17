#!/bin/bash
systemctl --user stop voicetyping-core 2> /dev/null
systemctl --user disable voicetyping-core 2> /dev/null
rm -f /home/deck/.config/systemd/user/voicetyping-core.service
