#!/bin/bash
# SISStateReportingManager - Start Application
# Starts both backend and frontend servers

set -e

cd "$(dirname "$0")"

echo "=========================================="
echo "Starting SISStateReportingManager"
echo "=========================================="

# Check if PostgreSQL is running
if command -v docker &> /dev/null; then
    if ! docker ps --format '{{.Names}}' | grep -q '^sis-postgres$'; then
        echo "Starting PostgreSQL..."
        docker start sis-postgres 2>/dev/null || echo "PostgreSQL container not found - run setup-local.sh first"
    fi
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Start backend in background
echo "Starting backend on http://localhost:8000..."
python -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend ready"
        break
    fi
    sleep 1
done

# Seed database if empty
STATE_COUNT=$(curl -s http://localhost:8000/api/states 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('total',0))" 2>/dev/null || echo "0")
if [ "$STATE_COUNT" = "0" ]; then
    echo "Seeding database..."
    python -m src.backend.seed_all 2>/dev/null || echo "Note: Some seed data may have failed"
fi

# Start frontend
echo "Starting frontend on http://localhost:3000..."
cd src/frontend
npm run dev &
FRONTEND_PID=$!
cd ../..

echo ""
echo "=========================================="
echo "✅ Application Running!"
echo "=========================================="
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Login password: admin123"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for Ctrl+C
trap "echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT
wait
