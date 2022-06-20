#! /bin/bash

opt="empty"
opt=$1


if [[ $opt == "" ]]; then
     ./Server.py
elif [[ $opt == "background" ]]; then
    ./Server.py passiv &
    SERVER_PID=$!
    echo $SERVER_PID >> .serverpid
    echo "Process has pid: " $SERVER_PID
elif [[ $opt == "normal" ]]; then
    ./Server.py
elif [[ $opt == "kill" ]]; then
    val=$(cat .serverpid) 
    echo "Killed " $val
    kill $val
    
else 
    echo "no such option"
fi
