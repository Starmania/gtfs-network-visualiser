function ctrl_c() {
    echo "** Trapped CTRL-C"
}

# Start the server
while true; do
    trap ctrl_c INT
    clear
    $(dirname "${BASH_SOURCE[0]}" )/run_simple_python.sh app.py
    echo "Server crashed. Restarting in 1 second..."
    trap - INT
    sleep 1
done
