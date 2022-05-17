#!/bin/bash



DESKTOP_MODESTRING=DESKTOP
GAMEMODE_MODESTRING=GAMEMODE

DESKTOP_PROCESS=startplasma-x11

LAST_MODE=$GAMEMODE_MODESTRING


restart_service() {
    echo "Restarting Voice Typing Service..."
    touch "LOCK"
    systemctl --user disable voicetyping-core.service
    sleep 15
    systemctl --user enable voicetyping-core.service
    rm "LOCK"
}

while true
do
    if ! pgrep -x "$DESKTOP_PROCESS" > /dev/null; then
        if [ $LAST_MODE != $GAMEMODE_MODESTRING ]; then
            restart_service
            LAST_MODE=$GAMEMODE_MODESTRING
        fi
    elif [ $LAST_MODE != $DESKTOP_MODESTRING ]; then
        restart_service
        LAST_MODE=$DESKTOP_MODESTRING
    fi
    sleep 1
done