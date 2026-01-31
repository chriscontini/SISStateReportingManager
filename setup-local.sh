#!/bin/bash
# SISStateReportingManager - Local Setup Script
# Run this on your local machine after cloning the repo

set -e

echo "=========================================="
echo "SISStateReportingManager Local Setup"
echo "=========================================="

# Check for required tools
echo ""
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Install from https://python.org"
    exit 1
fi
echo "✅ Python 3 found"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required. Install from https://nodejs.org"
    exit 1
fi
echo "✅ Node.js found"

if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found - you'll need to install PostgreSQL manually"
    USE_DOCKER=false
else
    echo "✅ Docker found"
    USE_DOCKER=true
fi

# Setup PostgreSQL
echo ""
echo "=========================================="
echo "Step 1: Setting up PostgreSQL"
echo "=========================================="

if [ "$USE_DOCKER" = true ]; then
    # Check if postgres container exists
    if docker ps -a --format '{{.Names}}' | grep -q '^sis-postgres$'; then
        echo "Starting existing PostgreSQL container..."
        docker start sis-postgres
    else
        echo "Creating PostgreSQL container..."
        docker run -d \
            --name sis-postgres \
            -e POSTGRES_USER=postgres \
            -e POSTGRES_PASSWORD=postgres \
            -e POSTGRES_DB=sis_manager \
            -p 5432:5432 \
            postgres:16
    fi

    echo "Waiting for PostgreSQL to be ready..."
    sleep 5

    # Create database if it doesn't exist
    docker exec sis-postgres psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'sis_manager'" | grep -q 1 || \
        docker exec sis-postgres psql -U postgres -c "CREATE DATABASE sis_manager"

    echo "✅ PostgreSQL ready"
else
    echo "Please ensure PostgreSQL is running on localhost:5432"
    echo "Database: sis_manager"
    echo "User: postgres"
    echo "Password: postgres"
    read -p "Press Enter when ready..."
fi

# Setup Python environment
echo ""
echo "=========================================="
echo "Step 2: Setting up Python backend"
echo "=========================================="

cd "$(dirname "$0")"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet \
    fastapi \
    uvicorn \
    sqlalchemy[asyncio] \
    asyncpg \
    pydantic-settings \
    python-jose[cryptography] \
    passlib[bcrypt] \
    aiohttp \
    numpy \
    anthropic

echo "✅ Python dependencies installed"

# Setup frontend
echo ""
echo "=========================================="
echo "Step 3: Setting up Next.js frontend"
echo "=========================================="

cd src/frontend
echo "Installing Node.js dependencies..."
npm install --silent
cd ../..

echo "✅ Frontend dependencies installed"

# Create .env if it doesn't exist
echo ""
echo "=========================================="
echo "Step 4: Creating configuration"
echo "=========================================="

if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sis_manager
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
DEBUG=false
EOF
    echo "✅ Created .env file"
else
    echo "✅ .env file already exists"
fi

# Done!
echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo ""
echo "  ./start-app.sh"
echo ""
echo "Or manually:"
echo "  Terminal 1: source venv/bin/activate && python -m uvicorn src.backend.main:app --port 8000"
echo "  Terminal 2: cd src/frontend && npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo "Password: admin123"
echo ""
