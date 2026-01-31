# Development Plan
# SISStateReportingManager

**Version**: 1.0
**Created**: 2026-01-29
**Timeline**: 12 Weeks (1-3 months)
**Status**: Planning

---

## Executive Summary

This document outlines the sprint-by-sprint development plan for SISStateReportingManager, an AI-powered state expansion planning tool for OnCourse Systems for Education.

**MVP Deliverables**:
1. State rankings for all 50 states (tiered analysis)
2. Gap analysis for top 3 states
3. Full knowledge base for top 3 states
4. AI chatbot for top 3 states
5. Executive dashboard
6. PDF/PowerPoint export

**Timeline**: 12 weeks / 6 two-week sprints

**Development Method**: Ralph autonomous AI agent loops

---

## Ralph Workflow

Each sprint is executed using [Ralph](https://github.com/snarktank/ralph) - an autonomous AI agent loop.

### How Ralph Works

1. **Iteration Start**: Fresh AI instance spawns with clean context
2. **Story Selection**: Picks highest-priority incomplete story from `prd.json`
3. **Implementation**: Implements the single story
4. **Quality Checks**: Runs type-checking and tests
5. **Commit**: If checks pass, commits changes
6. **Update**: Marks story complete in `prd.json`, appends learnings to `progress.txt`
7. **Repeat**: Loop continues until all stories pass

### Key Files

| File | Purpose |
|------|---------|
| `prd.json` | Task tracking - stories with `passes: true/false` |
| `progress.txt` | Learnings persisted across iterations |
| `CLAUDE.md` | Context for AI agents |

### Story Granularity

Stories must be small enough to complete in one context window:
- Add a database model
- Create an API endpoint
- Build a UI component
- Write a utility function

**Not**: "Build the entire dashboard" (too large)

### Sprint Transition

At end of each sprint:
1. Archive completed `prd.json` to `sprints/sprint-N-prd.json`
2. Create new `prd.json` for next sprint
3. Update `progress.txt` with sprint summary

---

## Technology Stack (Confirmed)

| Component | Technology | Notes |
|-----------|------------|-------|
| **Backend** | Python + FastAPI | Rapid development, strong AI ecosystem |
| **Database** | PostgreSQL | Relational with JSON support |
| **Vector DB** | pgvector (PostgreSQL extension) | Simplifies infrastructure |
| **LLM** | Claude API (Anthropic) | Stakeholder preference |
| **Frontend** | Next.js + React | Modern, SSR capable |
| **Styling** | Tailwind CSS | Rapid UI development |
| **Charts** | Recharts or Chart.js | Data visualization |
| **PDF Export** | React-PDF or Puppeteer | Report generation |
| **Frontend Hosting** | Netlify | Confirmed - excellent Next.js support |
| **Backend Hosting** | Railway or Render | Python/FastAPI + PostgreSQL |
| **Authentication** | Simple password | Internal tool; basic auth sufficient |

## Preliminary Target States (for early knowledge base work)

| Priority | State | Rationale |
|----------|-------|-----------|
| **#1** | Pennsylvania (PA) | Stakeholder identified |
| **#2** | Texas (TX) | Stakeholder identified |
| **#3** | Maryland (MD) | County-based (24 districts), large avg size, LA-like profile |

*Note: Final top 3 will be confirmed by ranking algorithm in Sprint 2, but PA, TX, and MD will receive early research attention.*

**Excluded**: Georgia (statewide PowerSchool contract)

---

## Sprint Overview

| Sprint | Weeks | Phase | Focus |
|--------|-------|-------|-------|
| Sprint 1 | 1-2 | Foundation | Infrastructure + Data Collection |
| Sprint 2 | 3-4 | Foundation | Ranking Algorithm + Initial Analysis |
| Sprint 3 | 5-6 | Core | Dashboard + Deep Analysis |
| Sprint 4 | 7-8 | Core | Gap Analysis + Validation |
| Sprint 5 | 9-10 | AI | Knowledge Base + RAG |
| Sprint 6 | 11-12 | AI | Chatbot + Reports + Polish |

---

## Phase 1: Foundation (Weeks 1-4)

### Sprint 1: Infrastructure & Data Collection (Weeks 1-2)

**Goal**: Set up development environment and build data collection pipeline for all 50 states.

#### Week 1 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-001** | Set up Git repository structure | 2h | P0 |
| **DEV-002** | Initialize Python/FastAPI backend project | 4h | P0 |
| **DEV-003** | Initialize Next.js frontend project | 4h | P0 |
| **DEV-004** | Set up PostgreSQL database with pgvector | 4h | P0 |
| **DEV-005** | Configure development environment (Docker) | 4h | P0 |
| **DEV-006** | Design database schema v1 | 4h | P0 |
| **DEV-007** | Create State model and CRUD operations | 4h | P1 |
| **DEV-008** | Research and document all 50 state DOE URLs | 8h | P0 |

#### Week 2 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-009** | Build web scraping framework for DOE sites | 8h | P0 |
| **DEV-010** | Implement NCES data integration | 6h | P0 |
| **DEV-011** | Create StateRequirement model | 4h | P1 |
| **DEV-012** | Build data ingestion pipeline | 8h | P0 |
| **DEV-013** | Collect Tier 1 data for 10 pilot states | 8h | P1 |
| **DEV-014** | Set up Claude API integration | 4h | P1 |
| **DEV-015** | Create basic API endpoints (states list) | 4h | P1 |

#### Sprint 1 Deliverables
- [ ] Development environment fully operational
- [ ] Database schema implemented
- [ ] Data collection pipeline working
- [ ] 10 states with Tier 1 data collected
- [ ] Basic API returning state list

#### Sprint 1 Definition of Done
- All developers can run the project locally
- Database migrations run successfully
- At least 10 states have basic data populated
- API endpoint `/api/states` returns data

---

### Sprint 2: Ranking Algorithm & Initial Analysis (Weeks 3-4)

**Goal**: Complete Tier 1 data collection for all 50 states and implement ranking algorithm.

#### Week 3 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-016** | Complete Tier 1 data collection (remaining 40 states) | 16h | P0 |
| **DEV-017** | Design ranking algorithm with weighted factors | 8h | P0 |
| **DEV-018** | Implement development effort estimation model | 8h | P0 |
| **DEV-019** | Create RankingFactor model and configuration | 4h | P1 |
| **DEV-020** | Build ranking calculation service | 8h | P0 |

#### Week 4 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-021** | Implement district structure analysis (county vs fragmented) | 6h | P1 |
| **DEV-022** | Add average district size calculations | 4h | P1 |
| **DEV-023** | Create competitive landscape basic scoring | 6h | P2 |
| **DEV-024** | Build API endpoint for rankings | 4h | P0 |
| **DEV-025** | Validate ranking against NJ/LA known data | 8h | P0 |
| **DEV-026** | Document ranking methodology | 4h | P1 |
| **DEV-027** | Create ranking factor weight configuration UI | 6h | P2 |

#### Sprint 2 Deliverables
- [ ] All 50 states with Tier 1 data
- [ ] Ranking algorithm implemented
- [ ] Development effort estimation working
- [ ] Rankings validated against NJ/LA
- [ ] API endpoint `/api/rankings` operational

#### Sprint 2 Definition of Done
- All 50 states ranked with composite scores
- NJ and LA appear at appropriate positions (validation)
- Ranking factors are configurable
- API returns sorted rankings with factor breakdowns

---

## Phase 2: Core Features (Weeks 5-8)

### Sprint 3: Dashboard & Deep Analysis (Weeks 5-6)

**Goal**: Build executive dashboard and perform Tier 2 deep analysis on top 10 states.

#### Week 5 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-028** | Design dashboard UI/UX wireframes | 6h | P0 |
| **DEV-029** | Build dashboard layout and navigation | 8h | P0 |
| **DEV-030** | Implement state rankings table component | 6h | P0 |
| **DEV-031** | Add sorting/filtering to rankings | 4h | P1 |
| **DEV-032** | Create state detail page | 8h | P0 |
| **DEV-033** | Begin Tier 2 deep analysis for top 10 states | 8h | P0 |

#### Week 6 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-034** | Complete Tier 2 analysis for top 10 states | 12h | P0 |
| **DEV-035** | Build comparison view (side-by-side states) | 8h | P1 |
| **DEV-036** | Implement data visualization (charts) | 8h | P1 |
| **DEV-037** | Add color-coded tier indicators | 4h | P2 |
| **DEV-038** | Create responsive mobile layout | 6h | P2 |
| **DEV-039** | Implement user authentication | 6h | P1 |

#### Sprint 3 Deliverables
- [ ] Functional executive dashboard
- [ ] State rankings with drill-down
- [ ] Comparison view for states
- [ ] Top 10 states with Tier 2 data
- [ ] Basic authentication

#### Sprint 3 Definition of Done
- Dashboard loads in < 3 seconds
- Users can sort/filter rankings
- Side-by-side comparison works for any 2 states
- Top 10 states have detailed data

---

### Sprint 4: Gap Analysis & Validation (Weeks 7-8)

**Goal**: Implement gap analysis module for top 3 states and validate system accuracy.

#### Week 7 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-040** | Design gap analysis data model | 4h | P0 |
| **DEV-041** | Implement NJ baseline capability mapping | 8h | P0 |
| **DEV-042** | Implement LA baseline capability mapping | 8h | P0 |
| **DEV-043** | Build gap comparison algorithm | 8h | P0 |
| **DEV-044** | Create gap analysis API endpoints | 4h | P0 |
| **DEV-045** | Begin Tier 3 comprehensive analysis for top 3 states | 8h | P0 |

#### Week 8 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-046** | Complete Tier 3 analysis for top 3 states | 12h | P0 |
| **DEV-047** | Build gap analysis visualization | 8h | P0 |
| **DEV-048** | Implement effort estimation display | 6h | P1 |
| **DEV-049** | Add timeline projection view | 6h | P1 |
| **DEV-050** | Stakeholder validation session | 4h | P0 |
| **DEV-051** | Refine rankings based on validation feedback | 8h | P1 |

#### Sprint 4 Deliverables
- [ ] Gap analysis for top 3 states
- [ ] NJ/LA baselines documented in system
- [ ] Effort estimation for each gap
- [ ] Validation complete with stakeholder sign-off
- [ ] Rankings refined based on feedback

#### Sprint 4 Definition of Done
- Gap analysis shows clear comparison to NJ/LA
- Effort estimates align with LA benchmark (2.5-3 years)
- Stakeholder (Chris) approves ranking methodology
- Top 3 states identified and confirmed

---

## Phase 3: AI Assistant (Weeks 9-12)

### Sprint 5: Knowledge Base & RAG (Weeks 9-10)

**Goal**: Build comprehensive knowledge base for top 3 states and implement RAG architecture.

#### Week 9 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-052** | Design knowledge base schema | 4h | P0 |
| **DEV-053** | Build document ingestion pipeline | 8h | P0 |
| **DEV-054** | Implement chunking strategy for state docs | 6h | P0 |
| **DEV-055** | Set up vector embeddings with pgvector | 6h | P0 |
| **DEV-056** | Collect all documentation for State #1 | 12h | P0 |
| **DEV-057** | Create source attribution system | 4h | P1 |

#### Week 10 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-058** | Collect all documentation for State #2 | 12h | P0 |
| **DEV-059** | Collect all documentation for State #3 | 12h | P0 |
| **DEV-060** | Implement hybrid search (semantic + keyword) | 8h | P0 |
| **DEV-061** | Build retrieval pipeline | 6h | P0 |
| **DEV-062** | Test retrieval accuracy | 4h | P1 |
| **DEV-063** | Create knowledge base admin interface | 6h | P2 |

#### Sprint 5 Deliverables
- [ ] Knowledge base populated for top 3 states
- [ ] Vector embeddings generated
- [ ] Retrieval pipeline operational
- [ ] Search returning relevant results
- [ ] Source attribution working

#### Sprint 5 Definition of Done
- Each of top 3 states has 50+ documents indexed
- Search returns relevant results with citations
- Retrieval latency < 2 seconds
- Sources are clearly attributed

---

### Sprint 6: Chatbot & Reports (Weeks 11-12)

**Goal**: Deploy AI chatbot and implement report generation. Final polish and launch.

#### Week 11 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-064** | Build chatbot UI component | 8h | P0 |
| **DEV-065** | Implement Claude API integration for chat | 6h | P0 |
| **DEV-066** | Create RAG prompt templates | 6h | P0 |
| **DEV-067** | Implement citation display in responses | 4h | P0 |
| **DEV-068** | Add conversation history | 6h | P1 |
| **DEV-069** | Build PDF report generation | 8h | P0 |
| **DEV-070** | Create PowerPoint export | 8h | P1 |

#### Week 12 Tasks

| Task | Description | Estimate | Priority |
|------|-------------|----------|----------|
| **DEV-071** | Test chatbot with dev team | 8h | P0 |
| **DEV-072** | Refine prompts based on testing | 6h | P0 |
| **DEV-073** | Design report templates | 6h | P1 |
| **DEV-074** | Implement exportable data (CSV) | 4h | P2 |
| **DEV-075** | Performance optimization | 6h | P1 |
| **DEV-076** | Security review | 4h | P1 |
| **DEV-077** | Documentation and handoff | 8h | P1 |
| **DEV-078** | Production deployment | 6h | P0 |

#### Sprint 6 Deliverables
- [ ] AI chatbot operational
- [ ] PDF report generation working
- [ ] PowerPoint export functional
- [ ] CSV data export available
- [ ] System deployed to production
- [ ] Documentation complete

#### Sprint 6 Definition of Done
- Chatbot answers state reporting questions accurately
- Citations appear in all responses
- Reports generate in < 30 seconds
- Dev team validates chatbot usefulness
- System is production-ready

---

## Risk Mitigation

### Technical Risks

| Risk | Mitigation | Contingency |
|------|------------|-------------|
| State DOE data inconsistent | AI-powered normalization | Manual curation for top states |
| Claude API rate limits | Implement caching, batching | Queue system for requests |
| Scraping blocked by DOEs | Respect robots.txt; use APIs where available | Manual data collection |
| RAG retrieval poor quality | Hybrid search; iterative tuning | Increase chunk overlap; rerank |

### Schedule Risks

| Risk | Mitigation | Contingency |
|------|------------|-------------|
| Data collection takes longer | Start with 10 pilot states | Reduce Tier 1 scope; prioritize top 20 |
| Ranking validation fails | Weekly stakeholder check-ins | Adjust algorithm iteratively |
| Chatbot quality insufficient | Extensive prompt engineering | Limit to FAQ-style responses |

---

## Resource Requirements

### Development Team

| Role | Allocation | Responsibilities |
|------|------------|------------------|
| **Full-Stack Developer** | 100% | Backend, frontend, integrations |
| **AI/ML Engineer** | 50-100% | RAG, embeddings, chatbot |
| **DevOps** | 25% | Infrastructure, deployment |
| **Product Owner** | 25% | Requirements, validation, acceptance |

### Infrastructure Costs (Estimated Monthly)

| Service | Estimated Cost |
|---------|---------------|
| Netlify (Frontend) | $0-19 (free tier likely sufficient) |
| Railway/Render (Backend + DB) | $20-50 |
| Claude API | $200-500 |
| Domain/SSL | $20 |
| **Total** | **$240-590/month** |

*Note: Costs are conservative estimates. Free tiers may cover initial usage.*

---

## Success Criteria by Phase

### Phase 1 Success (End of Week 4)
- [ ] All 50 states have Tier 1 data
- [ ] Rankings are generated
- [ ] NJ/LA validation passes
- [ ] API is operational

### Phase 2 Success (End of Week 8)
- [ ] Dashboard is functional
- [ ] Top 3 states identified
- [ ] Gap analysis complete
- [ ] Stakeholder approves rankings

### Phase 3 Success (End of Week 12)
- [ ] Chatbot answers questions accurately
- [ ] Reports generate correctly
- [ ] Dev team finds chatbot useful
- [ ] System is production-ready

---

## Open Questions for Sprint Planning

1. ~~**Hosting Decision**: AWS vs Vercel vs other?~~ **RESOLVED**: Netlify (frontend) + Railway/Render (backend)
2. ~~**Authentication**: Simple password vs OAuth vs SSO?~~ **RESOLVED**: Simple password
3. ~~**Top 3 States**: Should we pre-identify likely candidates for parallel knowledge base work?~~ **RESOLVED**: PA, TX, + 1 TBD
4. **Dev Team Access**: When should dev team start testing chatbot? *(Sprint 6, Week 11)*
5. ~~**Report Templates**: What specific data should appear in investor presentations?~~ **RESOLVED**: Expansion state recommendations

### Report Template Requirements
- **Primary Content**: Expansion state recommendations
- **Key Data Points**:
  - Ranked list of recommended states
  - Development effort estimates
  - Gap analysis summary
  - Competitive landscape overview
  - Projected timeline and investment

---

## Next Steps

1. [ ] Review and approve this development plan
2. [ ] Finalize hosting decision
3. [ ] Set up development environment
4. [ ] Begin Sprint 1

---

*Document Version: 1.0*
*Last Updated: 2026-01-29*
