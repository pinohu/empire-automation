#!/bin/bash

echo "🚀 Launching Empire Automation System"

# Start all services
echo "[1/6] Starting Docker services..."
docker-compose up -d

# Wait for services
echo "[2/6] Waiting for services to start..."
sleep 10

# Initialize if first time
if [ ! -f ".initialized" ]; then
    echo "[3/6] First time setup..."
    echo "  - Initializing database..."
    poetry run python empire_automation/database/init_db.py
    
    echo "  - Seeding database..."
    poetry run python empire_automation/database/seed_data.py
    
    touch .initialized
    echo "  [OK] Database initialized"
else
    echo "[3/6] System already initialized, skipping setup..."
fi

# Check if API is already running
echo "[4/6] Checking API status..."
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "  [OK] API already running on port 8000"
else
    echo "  [INFO] Starting API server..."
    poetry run uvicorn empire_automation.api.main:app --host 0.0.0.0 --port 8000 &
    sleep 3
    echo "  [OK] API started"
fi

# Check if Dashboard is already running
echo "[5/6] Checking Dashboard status..."
if curl -s http://localhost:8501 > /dev/null 2>&1; then
    echo "  [OK] Dashboard already running on port 8501"
else
    echo "  [INFO] Starting Dashboard..."
    poetry run streamlit run dashboard/app.py --server.port 8501 &
    sleep 3
    echo "  [OK] Dashboard started"
fi

# Verify services
echo "[6/6] Verifying services..."
sleep 2

echo ""
echo "✅ System launched!"
echo ""
echo "Services:"
echo "  📡 API:        http://localhost:8000"
echo "  📊 Dashboard:  http://localhost:8501"
echo "  🔄 n8n:        http://localhost:5678"
echo "  📚 API Docs:   http://localhost:8000/docs"
echo ""
echo "Next Steps:"
echo "  1. Open dashboard: http://localhost:8501"
echo "  2. Navigate to '90-Day Plan' page"
echo "  3. Execute Day 1 tasks"
echo "  4. Review daily briefing"
echo ""

