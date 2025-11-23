#!/bin/bash
# Backend Server Restart Script

echo "🔄 Restarting QIE Ticketing Backend Server..."

# Kill any existing server on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null
sleep 2

# Start the server
cd "$(dirname "$0")"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

