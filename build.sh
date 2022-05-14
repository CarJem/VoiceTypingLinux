#!/bin/bash
pyinstaller GoogleVoiceTypingPY.py
cp ToggleVoiceTyping.sh dist/GoogleVoiceTypingPY/ToggleVoiceTyping.sh
cp -r ./assets ./dist/GoogleVoiceTypingPY/assets/