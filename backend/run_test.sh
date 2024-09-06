#!/bin/env bash

set -eou pipefail

# Get the location of the script file
script_path=$(readlink -f "$0")
FILE_PATH=${script_path%/*}

set APP_ENV=test && set MYSQL_USER=localhost && "C:\Users\Adeyori\alx-project\backend\alx-venv\Scripts\python.exe" -m pytest "${FILE_PATH}\tests"

