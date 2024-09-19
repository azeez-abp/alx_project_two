#!/bin/env bash

set -eou pipefail

# Get the location of the script file
script_path=$(readlink -f "$0")
FILE_PATH=${script_path%/*}

# set APP_ENV=test && set MYSQL_USER=localhost && "${FILE_PATH}/alx_venv/Scripts/python.exe" -m pytest "${FILE_PATH}/tests"

 python -m unittest discover -s tests