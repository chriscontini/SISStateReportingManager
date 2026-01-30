# CLAUDE.md - AI Assistant Guide for SISStateReportingManager

This document provides guidance for AI assistants working with the SISStateReportingManager codebase.

## Project Overview

**SISStateReportingManager** is an AI-powered strategic expansion planning application for Student Information System (SIS) vendors. The application helps regional SIS companies identify and prioritize new state markets for expansion by analyzing state reporting requirements, competitive landscapes, and alignment with existing capabilities.

### Mission Statement

Enable regional SIS vendors to strategically grow their state footprint by:
1. Researching and comparing all 50 states' K-12 reporting requirements
2. Identifying states where existing capabilities can be most easily adapted
3. Building comprehensive knowledge bases and roadmaps for expansion
4. Supporting development teams with AI-powered assistance

### Current Status

**Sprint 6 Complete** - 100 stories implemented across 6 sprints.

The application is fully functional with:
- State rankings with 9 weighted scoring factors
- AI-powered analysis using Claude API
- Gap analysis comparing against NJ/LA baselines
- Implementation roadmaps with Gantt visualization
- Knowledge base with search
- Docker deployment ready
- 41 passing tests

## Core Application Modules

### 1. State Requirements Research Engine

**Purpose**: Aggregate and analyze K-12 state reporting requirements across all 50 states.

**Data Sources**:
- State Department of Education websites
- Official state reporting documentation
- State reporting user groups
- Online forums and communities
- Educational technology blogs
- CEDS (Common Education Data Standards) mappings

**Key Outputs**:
- Standardized state requirements database
- Data element catalogs per state
- Submission format specifications
- Compliance timelines and deadlines

### 2. Capability Matching System

**Purpose**: Compare state requirements against the SIS vendor's existing supported states and capabilities.

**Inputs**:
- Current supported state configurations
- Existing data models and schemas
- Current reporting functionality
- Technical architecture documentation

**Analysis**:
- Feature overlap percentage
- Data element coverage
- Process/workflow similarities
- Technical compatibility assessment

### 3. State Ranking Engine

**Purpose**: Rank all 50 states by expansion viability using weighted criteria.

**Ranking Factors**:
| Factor | Description |
|--------|-------------|
| **Technical Fit** | How closely existing code matches state requirements |
| **Data Element Overlap** | Percentage of required data already captured |
| **Process Similarity** | Alignment of submission workflows |
| **Competitive Landscape** | Density of established competitors |
| **Market Opportunity** | Number of districts, growth potential |
| **Hub Product Alignment** | Synergy with other company products (spokes) |
| **Regulatory Complexity** | Compliance burden and certification requirements |

**Output**: Ranked list of states with composite scores and factor breakdowns

### 4. Gap Analysis Module

**Purpose**: Perform detailed gap analysis for top-ranked states (Top 3).

**Analysis Components**:
- Missing data elements identification
- Required new processes/workflows
- Schema modifications needed
- Integration requirements
- Estimated development effort
- Risk assessment

### 5. Roadmap Generator

**Purpose**: Build comprehensive implementation roadmaps for target states.

**Roadmap Elements**:
- Phased implementation plan
- Data model modifications
- New feature development
- Testing and validation milestones
- Certification/approval timelines
- Resource requirements
- Dependencies and critical path

### 6. Knowledge Base Builder

**Purpose**: Create comprehensive knowledge repositories for target states.

**Content Aggregation**:
- Official state documentation
- User group discussions and insights
- Forum posts and community knowledge
- Blog articles and tutorials
- Historical requirement changes
- Common implementation challenges
- Best practices and lessons learned

**Knowledge Base Features**:
- Searchable document repository
- Categorized by topic/data element
- Version tracking for requirement changes
- Source attribution and reliability scoring

### 7. AI Development Assistant (Chatbot)

**Purpose**: Support the development team with AI-powered Q&A about state requirements.

**Capabilities**:
- Answer questions about state-specific requirements
- Explain data element definitions and mappings
- Provide code modification guidance
- Track new/changed requirements
- Compare requirements across states
- Suggest implementation approaches

### 8. Competitive Intelligence Module

**Purpose**: Analyze competitive landscape in target states.

**Analysis Areas**:
- National SIS vendors present in state
- Regional competitors and market share
- Vendor strengths and weaknesses
- Customer satisfaction indicators
- Pricing intelligence (where available)
- Partnership/integration ecosystems

### 9. Product Alignment Analyzer (Hub & Spoke)

**Purpose**: Evaluate how the company's full product portfolio aligns with state opportunities.

**Considerations**:
- Core SIS (Hub) fit with state requirements
- Complementary products (Spokes) that enhance value proposition
- Cross-sell opportunities
- Integration advantages
- Bundling strategies per state

## Repository Structure

```
SISStateReportingManager/
├── src/
│   ├── backend/                 # FastAPI backend
│   │   ├── routers/             # API endpoint handlers
│   │   │   ├── states.py        # State CRUD endpoints
│   │   │   ├── rankings.py      # Ranking endpoints
│   │   │   ├── gap_analysis.py  # Gap analysis endpoints
│   │   │   ├── roadmaps.py      # Roadmap endpoints
│   │   │   ├── knowledge.py     # Knowledge base endpoints
│   │   │   └── auth.py          # Authentication endpoints
│   │   ├── services/            # Business logic
│   │   │   ├── scoring_service.py    # 9-factor scoring
│   │   │   ├── claude_service.py     # Claude API integration
│   │   │   ├── gap_service.py        # Gap detection
│   │   │   ├── roadmap_service.py    # Roadmap generation
│   │   │   ├── knowledge_service.py  # Knowledge management
│   │   │   └── analysis_service.py   # Deep state analysis
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── baselines.py         # NJ/LA capability baselines
│   │   ├── nces_data.py         # NCES district/school data
│   │   ├── config.py            # Settings from env
│   │   ├── database.py          # Async DB connection
│   │   ├── middleware.py        # Error handling, logging
│   │   └── main.py              # FastAPI app entry
│   │
│   └── frontend/                # Next.js 14 frontend
│       └── src/
│           ├── app/             # App Router pages
│           │   ├── dashboard/   # Main dashboard
│           │   ├── states/      # State list and detail
│           │   ├── rankings/    # Rankings with weights config
│           │   ├── compare/     # State comparison
│           │   ├── gap-analysis/# Gap analysis views
│           │   ├── roadmap/     # Gantt chart roadmaps
│           │   ├── knowledge/   # Knowledge base search
│           │   └── login/       # Authentication
│           └── components/      # Reusable components
│               ├── charts/      # Recharts visualizations
│               ├── AppShell.tsx # Layout with nav
│               ├── AuthWrapper.tsx
│               ├── ExportButton.tsx
│               ├── KeyboardShortcuts.tsx
│               └── OnboardingTour.tsx
│
├── tests/                       # Test suites
│   ├── unit/                    # Service unit tests
│   ├── integration/             # API integration tests
│   └── test_rankings.py         # Ranking validation tests
│
├── docker-compose.yml           # Container orchestration
├── Dockerfile.backend           # Backend container
├── Dockerfile.frontend          # Frontend container
├── .env.example                 # Environment template
├── DEPLOYMENT.md                # Deployment guide
├── CLAUDE.md                    # This file
└── README.md                    # Project overview
```

## Development Guidelines

### Code Style Conventions

1. **Naming Conventions**
   - Use `camelCase` for variables and functions
   - Use `PascalCase` for classes and components
   - Use `SCREAMING_SNAKE_CASE` for constants
   - Use descriptive, domain-specific names (e.g., `stateRequirementParser`, `gapAnalysisReport`)

2. **File Organization**
   - One class/component per file
   - Group by feature/module, not by type
   - Keep files focused and under 300 lines when possible

3. **Documentation**
   - Add JSDoc/docstrings for all public APIs
   - Document complex algorithms and business logic
   - Include examples for non-obvious functionality

### Git Workflow

1. **Branch Naming**
   - Feature: `feature/<module>-<description>`
   - Bug fix: `fix/<module>-<description>`
   - AI assistant: `claude/<session-id>`

2. **Commit Messages**
   - Use conventional commits format
   - Reference module: `feat(ranking): add competitive density factor`
   - Keep first line under 72 characters

## Working with This Codebase

### For AI Assistants

When working on this project, understand these key domain concepts:

#### State Reporting Terminology

| Term | Definition |
|------|------------|
| **State Reporting** | Mandatory data submissions to state DOE |
| **Data Element** | Individual field required in state submissions |
| **Submission Window** | Time period for data collection/submission |
| **Validation Rules** | State-specific data quality requirements |
| **Certification** | State approval process for SIS vendors |
| **CEDS** | Common Education Data Standards (federal) |
| **Ed-Fi** | Education data standard and API specification |

#### SIS Vendor Context

- **Regional SIS Vendor**: Company serving specific geographic region
- **Hub Product**: Core SIS application
- **Spoke Products**: Complementary applications (LMS, Assessment, Finance, etc.)
- **State Footprint**: States where vendor is currently certified/operating

#### Key Implementation Considerations

1. **Data Accuracy**: State reporting data must be precise; errors can result in funding impacts
2. **Compliance Timelines**: States have strict submission deadlines
3. **Certification Requirements**: Many states require vendor certification
4. **FERPA Compliance**: All student data handling must comply with privacy laws
5. **Change Management**: State requirements change annually; system must adapt

### AI-Specific Features Development

When building AI components:

1. **Knowledge Base (RAG)**
   - Use chunking strategies appropriate for technical documentation
   - Maintain source attribution for all content
   - Implement version tracking for requirement changes
   - Consider hybrid search (semantic + keyword)

2. **Chatbot Development**
   - Ground responses in knowledge base content
   - Provide citations for requirement-related answers
   - Handle ambiguity by asking clarifying questions
   - Support comparison queries across states

3. **Research Automation**
   - Respect robots.txt and rate limits when scraping
   - Implement caching to avoid redundant requests
   - Validate extracted data against known schemas
   - Flag content that may be outdated

## Technology Stack Recommendations

Given the AI-heavy nature of this application:

### Backend
- **Python** (FastAPI/Flask) - Strong AI/ML ecosystem
- **PostgreSQL** - Relational data with JSON support
- **Redis** - Caching and session management

### AI/ML Components
- **LangChain/LlamaIndex** - RAG implementation
- **Vector Database** - Pinecone, Weaviate, or pgvector
- **Embeddings** - OpenAI, Cohere, or open-source models
- **LLM** - Claude API, OpenAI, or self-hosted

### Frontend (if applicable)
- **React/Next.js** - Modern web framework
- **TailwindCSS** - Utility-first styling
- **Chart.js/D3** - Data visualization

### Infrastructure
- **Docker** - Containerization
- **AWS/GCP/Azure** - Cloud hosting
- **GitHub Actions** - CI/CD

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sis_manager
REDIS_URL=redis://localhost:6379

# AI Services
ANTHROPIC_API_KEY=your-claude-api-key
OPENAI_API_KEY=your-openai-api-key
VECTOR_DB_URL=your-vector-db-url

# External APIs
STATE_DOE_API_KEYS={"CA": "key1", "TX": "key2"}

# Application
NODE_ENV=development
LOG_LEVEL=info
```

**Never commit actual credentials to version control.**

## Key Data Models (Implemented)

```python
# src/backend/models.py

State
├── id, name, abbreviation
├── doe_website, reporting_portal
├── total_districts, total_schools, total_students  # NCES data
└── certification_required

StateScore
├── state_id (FK)
├── factor_name (district_structure, avg_district_size, market_opportunity, etc.)
├── score (0-10)
├── weight (configurable)
├── tier (1/2/3, calculated)
└── composite_score (weighted sum)

StateAnalysis
├── state_id (FK)
├── analysis_type (tier2/competitive)
├── content (JSON - requirements, competitors, insights)
└── created_at

GapAnalysis
├── state_id (FK)
├── baseline_state (NJ or LA)
├── total_gaps, critical_gaps
├── total_effort_hours, projected_months
└── gaps[] (relationship to Gap model)

Gap
├── gap_analysis_id (FK)
├── category (data_element, workflow, integration, etc.)
├── description, severity
└── effort_hours

Roadmap
├── state_id (FK)
├── start_date, end_date
├── total_months, total_hours
└── phases[] (relationship to RoadmapPhase)

RoadmapPhase
├── roadmap_id (FK)
├── phase_number, name (Discovery, Development, Testing, etc.)
├── start_date, end_date, duration_months
├── effort_hours, fte_required
└── milestones[]

KnowledgeArticle
├── state_id (FK, nullable)
├── title, content, category
├── source_url, tags[]
└── created_at, updated_at
```

### Scoring Factors (9 total)

| Factor | Weight | Description |
|--------|--------|-------------|
| development_effort | 3.0 | PRIMARY - AI-estimated dev effort |
| technical_fit | 2.0 | Capability match with baselines |
| district_structure | 1.5 | County-based (LA) vs fragmented (NJ) |
| avg_district_size | 1.0 | Larger = higher ARPU |
| market_opportunity | 1.0 | Total students/districts |
| competitive_landscape | 1.0 | Fewer competitors = better |
| certification_complexity | 1.0 | Open market preferred |
| geographic_proximity | 0.5 | Distance from NJ HQ |
| data_element_overlap | 1.0 | Feature coverage |

## API Endpoints (Implemented)

```
# Authentication
POST /api/auth/login               # Login with password, returns JWT

# States
GET  /api/states                   # List all 50 states
GET  /api/states/{id}              # Get state by ID
GET  /api/states/{id}/detail       # Full state detail with NCES data
GET  /api/states/{id}/analysis     # Deep Tier 2 analysis
GET  /api/states/compare           # Compare multiple states (?ids=1,2,3)

# Rankings
GET  /api/rankings                 # Get ranked state list with scores
GET  /api/rankings/factors         # List all ranking factors with weights
PATCH /api/rankings/factors/{id}   # Update factor weight
POST /api/rankings/calculate       # Trigger score recalculation

# Gap Analysis
GET  /api/gap-analysis/{state_id}  # Get gap analysis for state
GET  /api/gap-analysis/{state_id}/gaps  # List individual gaps
POST /api/gap-analysis/{state_id}/analyze  # Run new analysis

# Roadmaps
GET  /api/roadmaps/{state_id}      # Get roadmap for state
POST /api/roadmaps/{state_id}/generate  # Generate new roadmap
PATCH /api/roadmaps/{id}/phases    # Update phase dates

# Knowledge Base
GET  /api/knowledge/articles       # List articles (filter by state)
GET  /api/knowledge/articles/{id}  # Get article detail
GET  /api/knowledge/search         # Search articles (?q=query)
POST /api/knowledge/articles       # Create new article

# System
GET  /health                       # Health check with DB status
GET  /api/admin/stats              # System statistics
```

## Resources

### State Reporting References
- [CEDS (Common Education Data Standards)](https://ceds.ed.gov/)
- [Ed-Fi Alliance](https://www.ed-fi.org/)
- [State DOE Directory](https://www2.ed.gov/about/contacts/state/index.html)

### Privacy & Compliance
- [FERPA Overview](https://www2.ed.gov/policy/gen/guid/fpco/ferpa/index.html)
- [Student Privacy Compass](https://studentprivacycompass.org/)

### Industry Resources
- [CoSN (Consortium for School Networking)](https://www.cosn.org/)
- [SETDA (State Educational Technology Directors Association)](https://www.setda.org/)

## The LA Benchmark

Louisiana serves as the success benchmark for state expansion:

- **30 months** development timeline
- **15,000 hours** total effort (100 productive hours/month × 5 FTE × 30 months)
- **5 FTE** average team size
- **6x higher ARPU** than NJ due to parish-based district model

States with similar county-based structures (like MD's 24 LEAs) score higher in `district_structure` factor.

## Key Commands

```bash
# Run tests
pytest

# Start with Docker
docker-compose up -d
docker-compose exec backend alembic upgrade head
docker-compose exec backend python -m src.backend.seed_all

# Manual backend start
cd src/backend
uvicorn main:app --reload

# Manual frontend start
cd src/frontend
npm run dev
```

---

*Last updated: 2026-01-30*
