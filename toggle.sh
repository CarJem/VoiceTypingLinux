#!/bin/bash
WAIT_FILE=WAIT
LOCK_FILE=LOCK
SCRIPT="python ./main_v2.py"

cd "$(dirname "$0")"

if test -f "$WAIT_FILE"; then
    rm "$WAIT_FILE"
    touch "$LOCK_FILE"
else
    $SCRIPT &
    touch "$WAIT_FILE"
fi