#! /bin/bash

opt=$1

HPATH=/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/
SPATH="${HPATH}Main.py"
WEBPATH="${HPATH}/WebInterface/app.py" 
U_PID="${HPATH}/WebInterface/.uipid"
PID="${HPATH}.serverpid"
UI_ENTRY="http://127.0.0.1:5000"

kill_func () {
    val=$(cat $PID) 
    kill $val
    rm  $PID
    echo "Killed ${val} (Server)" 
}

close_func () {
    val=$(cat $U_PID)
    kill $val
    rm $U_PID
    echo "Killed ${val} (UI)" 
}

is_alive () {
    if test -f $PID; then
        echo "Server is alive => (pid=$(cat $PID))"
        return 1
    else 
        echo "Server is not alive"
        return 0
    fi
}

is_open () {
    if test -f $U_PID; then
        echo "UI is alive =>  pid=($(cat $U_PID))"
        return 1
    else
        echo "UI is not alive"
        return 0
    fi
}





if [[ $opt == "help" ]]; then
    printf "background\n"
    printf "run(default)\n"
    printf "kill\n"
    printf "alive\n"
    printf "close\n"
    printf "ui\n"


elif [[ $opt == "background" ]]; then
    if ! test -f $PID; then
        ~/Desktop/Coding/Python/Homeserver/Main.py passiv & 
        SERVER_PID=$!
        echo $SERVER_PID > $PID
        echo "Process has pid: " $SERVER_PID
        exit
    else
        echo "Server already running.. ip=($(cat $PID))"
    fi


elif [[ $opt == "run" || $opt == "" ]]; then
    python3 $SPATH

elif [[ $opt == "ui" ]]; then
    python3 $WEBPATH &
    UI_PID=$!
    echo $UI_PID > $U_PID
    open $UI_ENTRY


elif [[ $opt == "kill" ]]; then
    kill_func

elif [[ $opt == "open" ]]; then
    open $UI_ENTRY

elif [[ $opt == "close" ]]; then
    close_func

elif [[ $opt == "closeall" ]]; then
    val=$(cat $U_PID)
    kill $val
    rm $U_PID
    echo "Killed ${val} (UI)" 
    
    val=$(cat $PID) 
    kill $val
    rm  $PID
    echo "Killed ${val} (Server)" 

elif [[ $opt == "alive" ]]; then
    is_alive
    is_open




else 
    echo "no such option"
fi
