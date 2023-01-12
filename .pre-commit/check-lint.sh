#!/bin/bash

BLUE='\033[1;34m'
RED='\033[0;31m'
NC='\033[0m'

printf "\n\n"
printf "${BLUE}Linting with black${NC}\n"
printf "\n"

if ! poetry run black --check ./modbus_connect/* ./tests/*
then
    lintfail=true
else
    lintfail=false
fi


if [ $lintfail = true ]
then
    printf "\n"
    printf "================ HELP ==================\n"

    printf "\n"
    printf "${RED}Reformat code${NC} with ${BLUE}poetry run black ./modbus_connect/* ./tests/* ${NC}\n"

    printf "\n"
    printf "========================================\n"
    # exit 1
fi