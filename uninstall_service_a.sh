#!/bin/bash

# SERVICE A
systemctl --user stop google_voice_typing_a 2> /dev/null
systemctl --user disable google_voice_typing_a 2> /dev/null
rm -f /home/deck/.config/systemd/user/google_voice_typing_a.service
