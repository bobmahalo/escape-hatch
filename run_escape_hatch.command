#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 main.py
echo ""
echo "Finished. You can safely close this window."
