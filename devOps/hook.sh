#!/bin/bash

#varibels
#env -> production / staging  
#branch -> billing / weight

env = "0"


case $1 in
    production) env = "1";;
    staging) env = "2";;
    *)  echo "error"; exit 1 ;;
esac

if [[ env -eq 2 ]]; then
    echo "working on staging auto diployment"
elif [[ env -eq 1 ]]; then
    echo "working on master auto diployment"
fi