#!/bin/bash
set -euo pipefail
while true; do
	REMOTE_NAME="keenetik" REMOTE_ROOT="ci" LOCAL_BASE="$HOME/cimeika" bash "$HOME/cit/home_node/ci_sync_loop.sh" >> "$HOME/cimeika/logs/ci_sync_loop.log" 2>&1 || true
	sleep 120
done
