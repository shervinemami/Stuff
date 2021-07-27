#!/bin/bash
# Show a '+' symbol and show every single command just before it's executed.
set -o xtrace

function kill_processes {
    # Kill each server, possibly with extra args passed to this function
    pkill $@ kaldi_module_loader_plus.py
    pkill $@ standalone_grids.py
    pkill $@ invisibleWindow.py
    pkill $@ bar-dragon-state-line
    pkill $@ xmacrorec2
    pkill $@ rsibreak
}

function kill_speechrec {
    # Give each server a chance for a clean exit
    kill_processes
    sleep 0.3s

    # Force all the servers to exit
    kill_processes -f -9
}

function stop_speechrec {
    echo "Closing all our Linux speechrec tools."
    zenity --notification --text="Stopping Kaldi and tools!"
    kill_speechrec

    rm -f /tmp/dragon-state.txt    # Clear the spoken history

    # Turn off the BlinkStick USB LED, if it's plugged in
    blinkstick off &>/dev/null || true
}

# First check if Kaldi speech recognition is already running. Keep this line of code in sync with "/Core/Custom/run_kaldi_child.sh"
# Since Kaldi is more likely to crash than standalone_grids is, do the check based on standalone_grids.
#/usr/bin/pgrep -f standalone_grids.py
#pidof kaldi_module_loader_plus.py
/usr/bin/pgrep -f kaldi_module_loader_plus.py
if [ $? -ne 0 ]; then
    echo "Starting Kaldi speech recognition on Linux."
    zenity --notification --text="Starting Kaldi and tools!"

    # Turn on the BlinkStick USB LED and show Purple that we're initializing, if it's plugged in
    blinkstick 050005 &>/dev/null || true

    # Start from fresh
    kill_speechrec

    # Run the mousegrid server
    (cd /Core/SpeechRec/aenea/server/linux_x11/ ; ./run_mousegrid_server.sh) &

    # Show 2 lines of recent commands, in the corner of the screen
    touch /tmp/dragon-state.txt ; chmod 600 /tmp/dragon-state.txt   # Stop other users from listening on all my spoken words!
    (cd /Core/polybar/build/bin ; (./polybar bar-dragon-state-line1 &) ; (./polybar bar-dragon-state-line2 &) )

    # Run RSIBreak after a while
    (sleep 20s && rsibreak &>/dev/null) &

    # Run speech recognition forever
    #export PYTHONIOENCODING=UTF-8
    (cd /Core/SpeechRec/Kaldi_Dragonfly/ ; python3 kaldi_module_loader_plus.py -r -s $@)
fi

# Kill the remaining processes
stop_speechrec

