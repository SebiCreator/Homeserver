#! /bin/bash

opt=$1

HPATH=/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/
SPATH="${HPATH}Server.py"
WEBPATH="${HPATH}/WebInterface/app.py" 
U_PID="${HPATH}/WebInterface/.uipid"
PID="${HPATH}.serverpid"

if [[ $opt == "help" ]]; then
    printf "background\n"
    printf "run(default)\n"
    printf "kill\n"
    printf "alive\n"
    printf "close\n"
    printf "ui\n"


elif [[ $opt == "background" ]]; then
    if ! test -f $PID; then
        ~/Desktop/Coding/Python/Homeserver/Server.py passiv & 
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
    open http://127.0.0.1:5000


elif [[ $opt == "kill" ]]; then
    val=$(cat $PID) 
    kill $val
    rm  $PID
    echo "Killed ${val} (Server)" 

elif [[ $opt == "open" ]]; then
    open http://127.0.0.1:5000

elif [[ $opt == "close" ]]; then
    val=$(cat $U_PID)
    kill $val
    rm $U_PID
    echo "Killed ${val} (UI)" 

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
    if test -f $PID; then
        echo "Server is alive => (pid=$(cat $PID))"
    else 
        echo "Server is not alive"
    fi

    if test -f $U_PID; then
        echo "UI is alive =>  pid=($(cat $U_PID))"
    else
        echo "UI is not alive"
    fi



else 
    echo "no such option"
fi
