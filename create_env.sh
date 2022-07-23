#! /bin/bash

RED='\033[0;31m'
NC='\033[0m'


virtualenv --python python3.9 venv
source venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip

pip list
printf "${RED}>>> Type \"source venv/bin/activate\" to activate the env${NC}\n"

