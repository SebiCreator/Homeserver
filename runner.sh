#! /bin/bash


ROOTPATH="/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver"
WEBSITE="http://127.0.0.1:5000"

SERVER_CMD=".${SERVERPATH}"

ui_alive () {
    if test -f ".ui_pid"; then
        echo "++ UI is alive ++\n"
    else 
        echo "-- UI is not alive --\n"
    fi
}

se_alive () {
    if test -f ".se_pid"; then
        echo "++ Server is alive ++\n"
    else 
        echo "-- Server is not alive --\n"
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
    printf "Help"

elif [[ $1 == "run-server" ]]; then
    se_start

elif [[ $1 == "run-ui" ]]; then
    ui_start
    open "$WEBSITE"

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