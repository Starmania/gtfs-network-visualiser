# Search for venv
venvs=$(find  . -maxdepth 2 -type f -name 'pyvenv.cfg' -exec dirname {} \;)
venv=$(echo $venvs | cut -d ' ' -f 1)

if [ -z "$venv" ]; then
    echo "No venv found. Please use a virtual environment for better support."
else
    echo "Found venv."
    echo "Venv path: $venv"
    source $venv/bin/activate
fi

python3 "$@"
