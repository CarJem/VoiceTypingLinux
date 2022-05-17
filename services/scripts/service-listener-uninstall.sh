#!/bin/bash
systemctl stop voicetyping-listener 2> /dev/null
systemctl disable voicetyping-listener 2> /dev/null
rm -f /etc/systemd/system/voicetyping-listener.service