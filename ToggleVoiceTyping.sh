#!/bin/bash
WAIT_FILE=WAIT
LOCK_FILE=LOCK
SCRIPT="./GoogleVoiceTypingPY"
DEV_SCRIPT="python ./GoogleVoiceTypingPY.py"

cd "$(dirname "$0")"

run_script() {
    if [ "$1" == "DEV" ]; then
        $DEV_SCRIPT &
    else
        $SCRIPT &
    fi
    touch "$WAIT_FILE"
}

if test -f "$WAIT_FILE"; then
    rm "$WAIT_FILE"
    touch "$LOCK_FILE"
else
    run_script "$1"
fi