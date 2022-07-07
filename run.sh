#! /bin/bash

opt=$1

if [[ $opt == "" ]]; then
    printf "background\n"
    printf "normal\n"
    printf "kill\n"
    printf "alive\n"


elif [[ $opt == "background" ]]; then
    ./Server.py passiv &
    SERVER_PID=$!
    echo $SERVER_PID > .serverpid
    echo "Process has pid: " $SERVER_PID


elif [[ $opt == "normal" ]]; then
    ./Server.py



elif [[ $opt == "kill" ]]; then
    val=$(cat .serverpid) 
    kill $val
    rm .serverpid
    echo "Killed " $val


elif [[ $opt == "alive" ]]; then
    if test -f ".serverpid"; then
        echo "Server is alive => (pid=$(cat .serverpid))"
    else 
        echo "Server is not alive"
    fi



else 
    echo "no such option"
fi
