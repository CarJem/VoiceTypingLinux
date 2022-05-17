#!/bin/bash
WAIT_FILE=WAIT
SEND_FILE=SEND
LOCK_FILE=LOCK
REQUEST_FILE=REQUEST
SCRIPT="./voice-typing"

cd "$(dirname "$0")"

manual_mode() {
    if test -f "$WAIT_FILE"; then
        rm "$WAIT_FILE"
        touch "$SEND_FILE"
    elif test -f "$LOCK_FILE"; then
        echo "Can't run multiple instances"
    else
        $SCRIPT &
        touch "$WAIT_FILE"
    fi
}

service_mode() {
    while true
    do
        if test -f "$REQUEST_FILE"; then
            rm -f "$REQUEST_FILE"
            manual_mode
        fi
        sleep 1
    done
}

if [ "$1" == "--SERVICE" ]; then
    service_mode
else
    manual_mode
fi
