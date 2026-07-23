#!/usr/bin/env bash
# Launch the Sun Meeting Buddy (macOS / Linux).
# Pass through any flags, e.g. ./run.sh --every 15 --now
cd "$(dirname "$0")" || exit 1
exec python3 buddy.py "$@"
