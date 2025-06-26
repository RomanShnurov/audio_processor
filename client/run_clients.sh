#!/bin/bash

echo "How many clients do you want to run?"
read num_clients

echo "Starting $num_clients clients..."

for i in $(seq 1 $num_clients); do
    echo "Starting client $i"
    uv run client/client.py > client/client_$i.log 2>&1 &
    client_pids[$i]=$!
done

echo "All clients started. PIDs: ${client_pids[*]}"
echo "Press Enter to stop all clients..."
read

# Kill all clients
for pid in "${client_pids[@]}"; do
    kill $pid 2>/dev/null
done

echo "All clients stopped"