#! /bin/bash

opt=$1

HPATH=/Users/sebastiankaeser/Desktop/Coding/Python/Homeserver/
SPATH="${HPATH}Server.py"
SPATH_="${HPATH}Server.py"
PID="${HPATH}.serverpid"

if [[ $opt == "" ]]; then
    printf "background\n"
    printf "normal\n"
    printf "kill\n"
    printf "alive\n"


elif [[ $opt == "background" ]]; then
    exec $SPATH &
    SERVER_PID=$!
    echo $SERVER_PID > $PID
    echo "Process has pid: " $SERVER_PID


elif [[ $opt == "normal" ]]; then
    python3 $SPATH



elif [[ $opt == "kill" ]]; then
    val=$(cat $PID) 
    kill $val
    rm  $PID
    echo "Killed " $val


elif [[ $opt == "alive" ]]; then
    if test -f $PID; then
        echo "Server is alive => (pid=$(cat $PID)"
    else 
        echo "Server is not alive"
    fi



else 
    echo "no such option"
fi
