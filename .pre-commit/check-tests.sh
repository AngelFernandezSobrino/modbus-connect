#!/bin/bash

BLUE='\033[1;34m'
RED='\033[0;31m'
NC='\033[0m'

if ! poetry run pytest
then
    testfail=true
else
    testfail=false
fi


if [ $testfail = true ]
then
    printf "\n"
    printf "================ HELP ==================\n"

    printf "\n"
    printf "${RED}Tests not passing, check commit${NC}\n"

    printf "\n"
    printf "========================================\n"
    # exit 1
fi