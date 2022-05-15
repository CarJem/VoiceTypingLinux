#!/bin/bash
WAIT_FILE=WAIT
SEND_FILE=SEND
LOCK_FILE=LOCK
REQUEST_FILE=REQUEST
SCRIPT="./GoogleVoiceTypingPY"
DEV_SCRIPT="python ./GoogleVoiceTypingPY.py"

cd "$(dirname "$0")"

manual_mode() {
    if test -f "$WAIT_FILE"; then
        rm "$WAIT_FILE"
        touch "$SEND_FILE"
    elif test -f "$LOCK_FILE"; then
        echo "Can't run multiple instances"
    else
        if [ "$1" == "--DEV" ]; then
            $DEV_SCRIPT &
        else
            $SCRIPT &
        fi
        touch "$WAIT_FILE"
    fi
}

service_mode() {
    while true
    do
        if test -f "$REQUEST_FILE"; then
            rm -f "$REQUEST_FILE"
            manual_mode "$1"
        fi
        sleep 1
    done
}

if [ "$1" == "--SERVICE" ]; then
    service_mode "$2"
else
    manual_mode "$1"
fi
