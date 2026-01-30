# SISStateReportingManager

AI-powered state expansion planning tool for Student Information System (SIS) vendors.

## Overview

SISStateReportingManager helps regional SIS vendors strategically expand into new state markets by:

- **Ranking all 50 states** by expansion viability using 9 weighted factors
- **Analyzing gaps** between current capabilities (NJ/LA baselines) and target state requirements
- **Generating roadmaps** with phased implementation plans and effort estimates
- **Building knowledge bases** of state-specific documentation and requirements

Built for [OnCourse Systems for Education](https://oncoursesystems.com) to support data-driven expansion decisions.

## Features

### State Rankings
- 9 scoring factors: development effort, technical fit, market opportunity, district structure, competitive landscape, etc.
- AI-powered scoring using Claude API
- Tier classification (1/2/3) for prioritization
- Configurable factor weights

### Gap Analysis
- Compare target states against NJ and LA baselines
- Identify missing features, workflows, and integrations
- Effort estimation in hours and FTE-months
- Severity classification (low/medium/high/critical)

### Implementation Roadmaps
- Phased implementation plans (Discovery, Development, Testing, Certification, Pilot, Rollout)
- Gantt chart visualization
- Resource allocation by phase
- LA benchmark comparison (30 months, 15,000 hours, 5 FTE)

### Knowledge Base
- State-specific documentation
- Search and filter by state/category
- Source attribution and tagging

## Tech Stack

**Backend**
- Python 3.11+ with FastAPI
- PostgreSQL with SQLAlchemy 2.0 (async)
- Alembic for migrations
- Claude API (Anthropic) for AI analysis

**Frontend**
- Next.js 14 with TypeScript
- Tailwind CSS
- Recharts for data visualization

**Infrastructure**
- Docker & Docker Compose
- JWT authentication

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Anthropic API key (optional, for AI features)

### Setup

```bash
# Clone repository
git clone <repository-url>
cd SISStateReportingManager

# Configure environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY and AUTH_PASSWORD

# Start services
docker-compose up -d

# Run migrations and seed data
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m src.backend.seed_all
```

### Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs

Default login password: `admin123` (change in production!)

## Project Structure

```
SISStateReportingManager/
├── src/
│   ├── backend/           # FastAPI backend
│   │   ├── routers/       # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── models.py      # SQLAlchemy models
│   │   └── baselines.py   # NJ/LA capability baselines
│   └── frontend/          # Next.js frontend
│       └── src/
│           ├── app/       # Pages (App Router)
│           └── components/ # React components
├── tests/                 # Test suites
├── docker-compose.yml     # Container orchestration
├── DEPLOYMENT.md          # Deployment guide
└── CLAUDE.md              # AI assistant guide
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/states` | List all states |
| `GET /api/rankings` | Get ranked state list |
| `POST /api/rankings/calculate` | Trigger score calculation |
| `GET /api/gap-analysis/{state_id}` | Get gap analysis |
| `GET /api/roadmaps/{state_id}` | Get implementation roadmap |
| `GET /api/knowledge/articles` | Search knowledge base |
| `POST /api/auth/login` | Authenticate |

Full API documentation available at `/docs` when running.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Alt+D` | Go to Dashboard |
| `Alt+S` | Go to States |
| `Alt+R` | Go to Rankings |
| `Alt+G` | Go to Gap Analysis |
| `Alt+M` | Go to Roadmap |
| `Alt+K` | Go to Knowledge Base |
| `Shift+?` | Show shortcuts help |

## Testing

```bash
# Run all tests
cd /path/to/SISStateReportingManager
pytest

# Run specific test file
pytest tests/test_rankings.py -v
```

## Development

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines and domain concepts.

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions.

## The LA Benchmark

Louisiana serves as our success benchmark:
- **30 months** development timeline
- **15,000 hours** total effort
- **5 FTE** team size
- **6x higher ARPU** than NJ due to parish-based model

States with similar county-based district structures (like MD's 24 LEAs) are prioritized for expansion.

## Status

**Sprint 6 Complete** - 100 stories implemented across 6 sprints

- State rankings with AI scoring
- Gap analysis with effort estimation
- Implementation roadmaps
- Knowledge base
- Docker deployment
- Dark mode, keyboard shortcuts, export functionality

## License

Proprietary - OnCourse Systems for Education
