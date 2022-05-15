#!/bin/bash

# SERVICE B

systemctl stop google_voice_typing_b 2> /dev/null
systemctl disable google_voice_typing_b 2> /dev/null
rm -f /etc/systemd/system/google_voice_typing_b.service