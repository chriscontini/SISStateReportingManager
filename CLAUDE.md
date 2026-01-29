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

This project is in the **initial development stage**. The repository has been initialized but does not yet contain implementation code.

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
├── README.md                    # Project overview
├── CLAUDE.md                    # This file - AI assistant guidance
└── .git/                        # Git version control
```

### Planned Architecture

```
SISStateReportingManager/
├── src/
│   ├── research/                # State requirements research engine
│   │   ├── scrapers/            # Web scraping for state docs
│   │   ├── parsers/             # Document parsing utilities
│   │   └── aggregators/         # Data consolidation
│   │
│   ├── matching/                # Capability matching system
│   │   ├── analyzers/           # Feature comparison logic
│   │   └── mappers/             # Data element mapping
│   │
│   ├── ranking/                 # State ranking engine
│   │   ├── criteria/            # Ranking factor definitions
│   │   ├── weights/             # Configurable weight system
│   │   └── calculators/         # Score computation
│   │
│   ├── gap-analysis/            # Gap analysis module
│   │   ├── comparators/         # Requirement comparison
│   │   └── reporters/           # Gap report generation
│   │
│   ├── roadmap/                 # Roadmap generator
│   │   ├── templates/           # Roadmap templates
│   │   └── generators/          # Dynamic roadmap creation
│   │
│   ├── knowledge-base/          # Knowledge base builder
│   │   ├── collectors/          # Content aggregation
│   │   ├── indexers/            # Search indexing
│   │   └── storage/             # Document storage
│   │
│   ├── chatbot/                 # AI development assistant
│   │   ├── embeddings/          # Vector embeddings
│   │   ├── retrieval/           # RAG implementation
│   │   └── agents/              # Conversational agents
│   │
│   ├── competitive/             # Competitive intelligence
│   │   ├── trackers/            # Competitor monitoring
│   │   └── analyzers/           # Market analysis
│   │
│   ├── product-alignment/       # Hub & spoke analyzer
│   │   └── evaluators/          # Product fit assessment
│   │
│   ├── api/                     # REST API endpoints
│   ├── models/                  # Data models
│   ├── services/                # Business logic services
│   ├── utils/                   # Utility functions
│   └── config/                  # Configuration management
│
├── data/
│   ├── states/                  # State-specific data
│   ├── requirements/            # Requirements databases
│   ├── knowledge/               # Knowledge base content
│   └── vendor/                  # Vendor capability data
│
├── tests/                       # Test suites
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/                        # Documentation
│   ├── architecture/
│   ├── api/
│   └── user-guides/
│
├── scripts/                     # Utility scripts
└── config/                      # Environment configs
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

## Key Data Models (Conceptual)

```
State
├── id, name, abbreviation
├── doeWebsite, reportingPortal
├── certificationRequired (bool)
└── reportingCalendar

StateRequirement
├── stateId, dataElementId
├── description, format
├── validationRules
├── submissionFrequency
└── effectiveDate, expirationDate

DataElement
├── id, name, cedsMapping
├── dataType, constraints
└── description

VendorCapability
├── dataElementId
├── supportedStates[]
├── implementationDetails
└── customizationRequired

GapAnalysis
├── targetStateId
├── missingElements[]
├── partialElements[]
├── estimatedEffort
└── riskLevel

Competitor
├── name, type (national/regional)
├── statesServed[]
├── strengths, weaknesses
└── marketShare (estimated)
```

## API Endpoints (Planned)

```
# State Research
GET  /api/states                    # List all states with basic info
GET  /api/states/:id/requirements   # State-specific requirements
POST /api/states/:id/refresh        # Trigger research refresh

# Ranking
GET  /api/ranking                   # Get ranked state list
POST /api/ranking/configure         # Update ranking weights
GET  /api/ranking/factors           # Available ranking factors

# Gap Analysis
POST /api/gap-analysis              # Generate gap analysis
GET  /api/gap-analysis/:stateId     # Get existing analysis

# Roadmap
POST /api/roadmap/generate          # Generate implementation roadmap
GET  /api/roadmap/:stateId          # Get existing roadmap

# Knowledge Base
GET  /api/knowledge/search          # Search knowledge base
POST /api/knowledge/ingest          # Add new content
GET  /api/knowledge/sources         # List content sources

# Chatbot
POST /api/chat                      # Send message to AI assistant
GET  /api/chat/history              # Get conversation history

# Competitive
GET  /api/competitive/:stateId      # Competitive analysis for state
GET  /api/competitive/national      # National competitor overview
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

---

*Last updated: 2026-01-29*
