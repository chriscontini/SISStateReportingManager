# Deployment Guide

This guide covers deploying SISStateReportingManager using Docker or manually.

## Prerequisites

- Docker and Docker Compose (for containerized deployment)
- Node.js 20+ (for manual frontend deployment)
- Python 3.11+ (for manual backend deployment)
- PostgreSQL 15+ with pgvector extension
- Redis 7+ (optional, for caching)

## Quick Start with Docker

### 1. Clone and Configure

```bash
# Clone the repository
git clone <repository-url>
cd SISStateReportingManager

# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

### 2. Configure Environment Variables

Edit `.env` with your production settings:

```env
# IMPORTANT: Change these in production!
AUTH_SECRET_KEY=your-secure-secret-key-at-least-32-chars
AUTH_PASSWORD=your-secure-password

# Optional: Add Anthropic API key for AI features
ANTHROPIC_API_KEY=your-api-key
```

### 3. Start Services

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 4. Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed initial data
docker-compose exec backend python -m src.backend.seed_all
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Manual Deployment

### Backend Setup

```bash
cd src/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/sis_manager
export AUTH_SECRET_KEY=your-secret-key
export AUTH_PASSWORD=admin123

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd src/frontend

# Install dependencies
npm install

# Set environment variables
export NEXT_PUBLIC_API_URL=http://localhost:8000

# Build for production
npm run build

# Start production server
npm start
```

## Database Setup

### PostgreSQL with pgvector

```sql
-- Create database
CREATE DATABASE sis_manager;

-- Connect to database
\c sis_manager

-- Enable pgvector extension (for future AI features)
CREATE EXTENSION IF NOT EXISTS vector;
```

### Running Migrations

```bash
# From backend directory
cd src/backend

# Create new migration (development)
alembic revision --autogenerate -m "description"

# Apply all migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `AUTH_SECRET_KEY` | JWT signing secret | - | Yes |
| `AUTH_PASSWORD` | Login password | `admin123` | Yes |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `http://localhost:3000` | No |
| `ANTHROPIC_API_KEY` | Claude API key for AI features | - | No |
| `REDIS_URL` | Redis connection string | - | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |

## Production Checklist

### Security

- [ ] Change `AUTH_SECRET_KEY` to a secure random value
- [ ] Change `AUTH_PASSWORD` to a strong password
- [ ] Use HTTPS in production
- [ ] Set proper `CORS_ORIGINS` for your domain
- [ ] Configure firewall rules
- [ ] Enable rate limiting (reverse proxy)

### Database

- [ ] Use strong database credentials
- [ ] Enable SSL for database connections
- [ ] Set up automated backups
- [ ] Configure connection pooling

### Monitoring

- [ ] Set up health check monitoring
- [ ] Configure log aggregation
- [ ] Set up alerting for errors
- [ ] Monitor resource usage

### Performance

- [ ] Enable Redis caching
- [ ] Configure CDN for static assets
- [ ] Set up database query caching
- [ ] Enable gzip compression

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml - scale backend
docker-compose up -d --scale backend=3
```

Use a load balancer (nginx, traefik) in front of multiple backend instances.

### Database Scaling

For high traffic:
- Use read replicas for read-heavy operations
- Consider connection pooling with PgBouncer
- Use Redis for session storage and caching

## Troubleshooting

### Common Issues

**Database connection fails:**
```bash
# Check database is running
docker-compose ps db

# Check connection string
docker-compose exec backend python -c "from src.backend.database import get_engine; print('OK')"
```

**Frontend can't reach backend:**
```bash
# Check CORS settings
curl -I http://localhost:8000/health

# Verify NEXT_PUBLIC_API_URL is set correctly
```

**Migrations fail:**
```bash
# Check current migration state
alembic current

# Check for pending migrations
alembic heads

# Force specific migration
alembic stamp head
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connectivity (from backend container)
docker-compose exec backend python -c "
from src.backend.database import get_engine
import asyncio

async def check():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.execute('SELECT 1')
    print('Database OK')

asyncio.run(check())
"
```

## Backup and Recovery

### Database Backup

```bash
# Backup
docker-compose exec db pg_dump -U postgres sis_manager > backup.sql

# Restore
docker-compose exec -T db psql -U postgres sis_manager < backup.sql
```

### Full System Backup

```bash
# Stop services
docker-compose stop

# Backup volumes
docker run --rm -v sis_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres-backup.tar.gz /data

# Restart services
docker-compose start
```

## Support

For issues and questions:
- Check the [API Documentation](http://localhost:8000/docs)
- Review logs: `docker-compose logs -f`
- Open an issue on GitHub
