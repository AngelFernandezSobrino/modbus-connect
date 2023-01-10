#!/bin/bash

BLUE='\033[1;34m'
RED='\033[0;31m'
NC='\033[0m'

if ! poetry run pytest
then
    $testfail = true
fi


if ! poetry run black --check ./modbus_connect/* ./tests/*
then
    $lintfail = true
fi

echo "Tests"

echo $testfail

echo "Lintfail"

echo $lintfail

if [ $testfail = true ] || [ $lintfail = true ]
then
    printf "\n"
    printf "================ HELP ==================\n"
fi

if [ $testfail = true ]
then
    printf "\n"
    printf "${RED}Tests not passing, check commit${NC}\n"
fi

if [ $lintfail = true ]
then
    printf "\n"
    printf "${RED}Reformat code${NC} with ${BLUE}poetry run black ./modbus_connect/* ./tests/* ${NC}\n"
fi

if [ $testfail = true ] || [ $lintfail = true ]
then
    printf "\n"
    printf "========================================\n"
    exit 1
fi