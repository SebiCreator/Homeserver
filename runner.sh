#! /bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'


ROOTPATH="/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver"
WEBSITE="http://127.0.0.1:5000"


ui_alive () {
    cd "$ROOTPATH"
    if test -f ".ui_pid"; then
        echo "${GREEN}++ UI is alive ++${NC}\n"
    else 
        echo "${RED}-- UI is not alive --${NC}\n"
    fi
}

se_alive () {
    cd "$ROOTPATH"
    if test -f ".se_pid"; then
        echo "${GREEN}++ Server is alive ++${NC}\n"
    else 
        echo "${RED}-- Server is not alive --${NC}\n"
    fi
}

ui_start() {
    cd "$ROOTPATH"
    if test -f ".ui_pid"; then
        printf "UI still active\n"
    else
        ./UI.py& >/dev/null
        echo $! > .ui_pid 
        printf "UI started..\n"
        open "$WEBSITE"
    fi
}

se_start() {
    cd "$ROOTPATH"
    if test -f ".se_pid"; then
        printf "Server still active\n"
    else
        ./Server.py passiv&
        echo $! > .se_pid
        printf "Server started..\n"
    fi
}

ui_kill() {
cd "$ROOTPATH"
    if test -f ".ui_pid"; then
        kill $(cat .ui_pid)
        rm .ui_pid
        printf "Killed UI-Process\n"
    else
        printf "keine UI-PID vorhanden\n"
    fi
}

se_kill() {
    cd "$ROOTPATH"
    if test -f ".se_pid"; then
        kill $(cat .se_pid)
        rm .se_pid
        printf "Killed Server Process\n"
    else 
        printf "keine Server-PID vorhanden\n"
    fi
}


if [[ $1 == "help" ]]; then
    echo "run-server -> runs server"
    echo "run-ui -> runs ui"
    echo "listen -> watching packets"
    echo "open -> opens ui (if running)"
    echo "kill-ui -> deactivates ui"
    echo "kill-server -> deactivates server"
    echo "proc -> shows what runs"
    echo "run-all -> runs server and ui"
    echo "kill-all -> kills server and ui"


elif [[ $1 == "run-server" ]]; then
    se_start

elif [[ $1 == "run-ui" ]]; then
    ui_start

elif [[ $1 == "listen" ]]; then
    cd "$ROOTPATH"; ./Server.py listen

elif [[ $1 == "" || $1 == "run" ]]; then
    cd "$ROOTPATH"; ./Server.py

elif [[ $1 == "open" ]]; then
    open "$WEBSITE"

    
elif [[ $1 == "kill-ui" ]]; then
    ui_kill    

elif [[ $1 == "kill-server" ]]; then
    se_kill
    

elif [[ $1 == "proc" ]]; then
    ui_alive
    se_alive

elif [[ $1 == "run-all" ]]; then
    se_start
    ui_start

elif [[ $1 == "kill-all" ]]; then
    se_kill
    ui_kill

else 
    printf "No such option as $1"
fi
