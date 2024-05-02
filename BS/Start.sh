#!/bin/bash

# Function to get IP address of connected LAN
get_lan_ip() {
    ip route get 1 | awk '{print $7; exit}'
}

# Get LAN IP address
lan_ip=$(get_lan_ip)

if [ -z "$lan_ip" ]; then
    echo "Error: Unable to retrieve LAN IP address."
    exit 1
fi

# Run Python script with LAN IP address
python_script="opencvserver.py"
python3 "$python_script" "$lan_ip"
