#!/bin/bash

#!/bin/bash

# Define the paths to your Python scripts
script1="test_scripts/call.py"
script2="test_scripts/call.py"
script3="test_scripts/call.py"
script4="test_scripts/call.py"
script5="test_scripts/call.py"
script6="test_scripts/call.py"
script7="test_scripts/call.py"
script8="test_scripts/call.py"
script9="test_scripts/call.py"
script10="test_scripts/call.py"

# Run the scripts in the background
python3 "$script1" &
python3 "$script2" &
python3 "$script3" &
python3 "$script4" &
python3 "$script5" &

# Wait for all scripts to finish
wait
