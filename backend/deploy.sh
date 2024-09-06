
set -oeu

$(which python)  -m venv venv


if [[ -d 'venv/Scripts'  ]]; then 
    venv/Scripts/activate
fi

"venv\Scripts\pip.exe" install -r  requirements.txt

flask --app app.app run --debug





