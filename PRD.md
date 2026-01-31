# Product Requirements Document (PRD)
# SISStateReportingManager

**Version**: 1.0
**Last Updated**: 2026-01-29
**Status**: Discovery Complete - Ready for Development Planning

---

## 1. Executive Summary

SISStateReportingManager is an AI-powered strategic expansion planning tool for **OnCourse Systems for Education**, a 25-year-old K-12 EdTech SaaS company. The application will help OnCourse identify and prioritize new state markets for SIS expansion by analyzing state reporting requirements, competitive landscapes, and alignment with existing capabilities.

**Key Business Context**:
- OnCourse serves 254 K-12 educational organizations (115 SIS customers)
- Current ARR: ~$7.6M with 95% recurring revenue
- Geographic concentration: NJ (60%), LA (37%), DC/GA (3%)
- Active M&A process creates urgency for demonstrating credible expansion roadmap
- Louisiana expansion model (6x ARPU vs NJ) proves geographic expansion value

**Project Scope**:
- **Timeline**: 1-3 months to demonstrate value
- **Budget**: No constraints
- **Build Approach**: Custom development (team/contractor/AI-assisted)
- **MVP**: State rankings + gap analysis + knowledge base + AI chatbot for top 3 states

## 2. Problem Statement

### 2.1 Current Challenges

| Challenge | Description | Business Impact |
|-----------|-------------|-----------------|
| **Research Time & Compliance Complexity** | Each state has unique reporting requirements. Deep expertise in NJSMART and EdLink/LDOE took years to build. | 2-3 years development and certification for new state entry |
| **Development Cost Uncertainty** | State-specific reporting modules require significant engineering investment without clear ROI visibility | Louisiana entry (2020) required dedicated resources; need predictability |
| **Competitive Intelligence Gaps** | Unknown: which districts use which vendors, contract cycles, decision-maker contacts | Manual research is time-prohibitive |
| **Sales Capacity Constraints** | 4 sales staff covering 745 districts across core markets | Limited resources require precise targeting |
| **Prioritization Decisions** | 632 untapped districts (85% whitespace) in current markets | Geographic expansion vs. market deepening ROI unclear |

### 2.2 Target Users

| User Role | Primary Use Case | Tool Component | Frequency |
|-----------|------------------|----------------|-----------|
| **Executive Leadership** (CEO, Partners) | Strategic state prioritization; M&A discussions | Dashboard, Reports | Weekly/Monthly |
| **Development Team** | Technical requirements; implementation guidance | AI Chatbot, Knowledge Base | Daily (post-state selection) |
| **Product Management** | Roadmap planning; feature prioritization | Gap Analysis, Roadmap | Weekly |
| **Sales Team** | Competitive positioning; target districts | Competitive Intel | As needed |

**Primary Users**:
- **Phase 1 (Ranking)**: Executive leadership
- **Phase 2 (Implementation)**: Development team (AI chatbot users)

## 3. Product Vision & Goals

### 3.1 Vision Statement

Enable OnCourse to make data-driven state expansion decisions by providing comprehensive intelligence on state reporting requirements, competitive landscapes, and development effort—transforming a 2-3 year research process into weeks.

### 3.2 Success Definition

> *"This tool is exactly what we needed"* when:
> 1. AI determines the optimal states for expansion based on development effort analysis
> 2. AI chatbot becomes a deep expert on all things state reporting for chosen states
> 3. Rankings are validated against NJ and LA experience with specific data thresholds

### 3.3 Success Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| **State Analysis Time** | < 2 weeks per state (vs. months) | Accelerate expansion planning |
| **Expansion Decision Confidence** | Quantified scoring for all 50 states | Remove gut-feel from strategic decisions |
| **Development Estimation Accuracy** | Gap analysis within 20% of actual effort | Better resource planning |
| **M&A Readiness** | Documented expansion roadmap for top 3-5 states | Support valuation discussions |
| **Louisiana-like Opportunity Identification** | Identify states with similar ARPU potential | Replicate 6x ARPU success |
| **Dev Team Productivity** | Faster answers to state reporting questions | AI chatbot accelerates development |

### 3.4 Strategic Context

**M&A Timeline Consideration**: OnCourse is preparing for potential transaction with PE or strategic buyers. Key value drivers:
- Demonstrating credible multi-state expansion roadmap impacts valuation
- Revenue multiple arbitrage between regional and national platforms
- Capital deployment plan ready for Day 1 post-close
- **Timeline**: 1-3 months to show demonstrable value

## 4. User Personas

### 4.1 Strategic Decision Maker (Primary - Phase 1)
- **Role**: CEO / Managing Partner (Chris Contini)
- **Goals**: Identify highest-ROI expansion states; build investor-ready growth story
- **Pain Points**: Lack of data-driven framework; time constraints; risk of wrong state choice
- **Success Criteria**: Confident, defensible expansion recommendations with clear rationale
- **Tool Usage**: Dashboard for rankings; PDF/PowerPoint for presentations

### 4.2 Technical/Financial Leader
- **Role**: CFO/CTO (Mark Yelcick)
- **Goals**: Assess technical feasibility; approve budget; validate ROI assumptions
- **Pain Points**: Unknown development costs for new states; infrastructure implications
- **Success Criteria**: Clear cost estimates; technical risk assessment
- **Tool Usage**: Gap analysis reports; effort estimates

### 4.3 Development Team Member (Primary - Phase 2)
- **Role**: Engineer on state reporting implementation
- **Goals**: Quickly understand new state requirements; find answers to technical questions
- **Pain Points**: Scattered documentation; no single source of truth for state specs
- **Success Criteria**: AI chatbot answers questions accurately with citations
- **Tool Usage**: AI chatbot for Q&A; knowledge base for deep research

### 4.4 Technical Architect
- **Role**: Lead Systems Architect (Joe Geary)
- **Goals**: Estimate complexity; plan technical implementation
- **Pain Points**: Scattered state specs; unknown integration requirements
- **Success Criteria**: Comprehensive technical requirements; validated effort estimates
- **Tool Usage**: Gap analysis; AI chatbot for technical deep-dives

## 5. Functional Requirements

### 5.1 State Requirements Research Engine

**Purpose**: Aggregate and analyze K-12 state reporting requirements across all 50 states.

**Key Insight from Discovery**: OnCourse's field mappings exist in code but there's no consolidated external dictionary. The tool must research new state requirements from external DOE sources, not rely on pre-built mappings.

**Research Approach**: Tiered
- **Tier 1 (All 50 states)**: Shallow analysis for initial ranking
- **Tier 2 (Top 10 states)**: Deeper analysis for refined ranking
- **Tier 3 (Top 3 states)**: Comprehensive knowledge base for implementation

**Data Sources to Aggregate**:
- State Department of Education websites
- Official state reporting documentation
- State reporting user groups
- Online forums and communities
- Educational technology blogs
- CEDS (Common Education Data Standards) mappings

**Required Outputs**:
- Standardized state requirements database
- Data element catalogs per state
- Submission format specifications (file types, APIs, portals)
- Compliance timelines and deadlines
- Certification requirements and processes

### 5.2 Capability Matching System

**Purpose**: Compare state requirements against OnCourse's existing NJ and LA implementations.

**Baseline Capabilities** (from discovery):

| Capability | NJ (NJSLEDS) | LA (LDOE/EdLink) |
|------------|--------------|------------------|
| Years of Experience | 20+ years | 5+ years (since 2020) |
| Active Customers | 104 SIS districts | 9 SIS parishes |
| Certification Status | Established, certified | Certified vendor |
| Reporting System | NJSLEDS (upgraded from NJSMART) | EdLink data exchange |
| Submission Format | Portal-based file uploads | Formal vendor certification + data exchange |
| Collection Cycles | Fall, Spring, EOY | Parish-specific cadences |

**Matching Analysis Required**:
- Feature overlap percentage vs. new state
- Data element coverage comparison
- Process/workflow similarities
- Technical compatibility assessment
- Certification process comparison (NJ vs LA vs target state)

### 5.3 State Ranking Engine

**Purpose**: Rank all 50 states by expansion viability using weighted criteria.

**PRIMARY RANKING FACTOR**: Development effort required to build state reporting requirements and validation. This is the key driver for all prioritization decisions.

**Ranking Factors**:

| Factor | Weight | Description | Data Source |
|--------|--------|-------------|-------------|
| **Development Effort** | **Critical** | Amount of work to build state reporting/validation | DOE documentation analysis |
| **District Structure** | High | Parish/county model (like LA) vs fragmented districts (like NJ) | NCES data |
| **Average District Size** | High | Larger districts = higher ARPU potential | NCES data |
| **Technical Fit** | High | How closely existing NJ/LA code matches state requirements | DOE documentation |
| **Certification Complexity** | Medium | Formal vendor certification vs. open market | DOE documentation |
| **Competitive Landscape** | Medium | Density of national/regional competitors | Market research |
| **Market Opportunity** | Medium | Total addressable market; growth potential | NCES data |
| **Regulatory Complexity** | Medium | Compliance burden beyond core reporting | DOE documentation |
| **Geographic Proximity** | Low | Ease of support and relationship building | Geography |

**Validation Requirement**: Rankings must be validated against NJ and LA experience with specific data thresholds to ensure model accuracy.

**"Louisiana-like" Profile to Identify**:
- Consolidated district structure (county/parish model)
- Large average district size (10K+ students)
- Formal vendor certification (creates barrier to entry once achieved)
- Relationship-driven compliance culture
- Full-suite adoption potential

### 5.4 Gap Analysis Module

**Purpose**: Perform detailed gap analysis for top-ranked states (Top 3).

**Analysis Components** (informed by LA implementation experience):

| Gap Category | Analysis Required | LA Benchmark |
|--------------|-------------------|--------------|
| **Data Elements** | Missing fields, format differences | 12-18 months to map |
| **Certification Process** | Timeline, requirements, relationships | 12-18 months for LDOE |
| **Performance/Scale** | Infrastructure needs for larger districts | Significant for 22K+ student districts |
| **Support Model** | Dedicated state resources needed | Required LA-specific support |
| **Integration Standards** | SIF, Ed-Fi, state-specific APIs | EdLink compliance |

**Effort Estimation Framework** (based on LA timeline):

| Phase | Duration | Activities |
|-------|----------|------------|
| Market Research & Decision | ~6 months | Target assessment, go/no-go |
| State Certification | ~12-18 months | Technical certification, relationship building |
| First Sales Cycle | ~6-12 months | RFP, demos, board approvals |
| Implementation | ~6-12 months | Data migration, configuration, training |
| **Total** | **~2.5-3 years** | Decision to first live submission |

### 5.5 Roadmap Generator

**Purpose**: Build comprehensive implementation roadmaps for target states.

**Roadmap Elements**:
- Phased implementation plan (mirroring LA timeline)
- Data model modifications required
- New feature development scope
- Testing and validation milestones
- Certification/approval timelines
- Resource requirements (dev, support, sales)
- Dependencies and critical path
- Investment requirements and payback period

### 5.6 Knowledge Base Builder

**Purpose**: Create comprehensive knowledge repositories for target states (Top 3).

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
- Comparison views across states

**Maintenance Model**: Combination of Knowledge Management team (9 staff) and development team responsibility.

### 5.7 AI Development Assistant (Chatbot)

**Purpose**: Support the development team with AI-powered Q&A about state requirements.

**Key Design Principle**: The chatbot is a **deep expert on chosen states** (1-2 states post-ranking), not a shallow generalist across all 50 states. It should know "all things state reporting" for the selected expansion targets.

**Users**: Development team only (not executives or sales)

**Capabilities**:
- Answer questions about state-specific requirements
- Explain data element definitions and mappings
- Compare requirements across states (NJ vs LA vs target)
- Provide implementation guidance based on LA experience
- Track new/changed requirements
- Surface relevant knowledge base content with citations

**Example Queries**:
- "What data elements does [State] require for special education reporting?"
- "How does [State]'s submission process compare to Louisiana's?"
- "What changed in [State]'s requirements this year?"
- "Estimate development effort for [State] based on our LA experience"

**Technology**: Claude (Anthropic) - preferred LLM

**Trust Level**: High - AI recommendations with citations are sufficient for technical decisions

### 5.8 Competitive Intelligence Module

**Purpose**: Analyze competitive landscape in target states.

**Competitor Scope**: Both national and regional players

**National Competitors to Track**:
- PowerSchool
- Infinite Campus
- Tyler Technologies
- Follett
- Others as identified

**Analysis Areas** (all requested):
- Market share estimates by state
- Known customer lists
- Pricing intelligence (where available)
- Product feature comparisons
- Contract renewal timing (where discoverable)
- Customer satisfaction / NPS data
- Partnership/integration ecosystems

**Key Context**: OnCourse has lost <$12K annual revenue to national competitors—strong regional moat. Need to identify states where regional advantages translate.

### 5.9 Product Alignment Analyzer (Hub & Spoke)

**Purpose**: Evaluate how OnCourse's full product portfolio aligns with state opportunities.

**Product Portfolio Analysis**:

| Product | Revenue | State Compliance? | Expansion Consideration |
|---------|---------|-------------------|------------------------|
| **SIS (Hub)** | $2.12M | Critical - core state reporting | Must-have for any new state |
| **Evaluate** | $1.04M | Significant - teacher eval frameworks | TEACHNJ equivalent in target state? |
| **Assessment** | $915K | Moderate - standards alignment | State standards alignment needed |
| **Classroom (LMS)** | $567K | None - state-agnostic | Cross-sell opportunity |
| **Analytics** | $315K | None - configurable | Cross-sell opportunity |
| **Data Manager** | $303K | None - internal workflows | Cross-sell opportunity |
| **MTSS** | $101K | Moderate - intervention tracking | Growing state requirements |

**Strategic Insight**: SIS customers are 3.1x more valuable and adopt 4.2x more products. Prioritize SIS compliance first—spokes follow.

**Lafourche Parish Model**: Started with Assessment ($103K) → Added SIS, LMS, Evaluate → Grew to $282K (174% growth in one year). Tool should identify similar land-and-expand opportunities.

## 6. Non-Functional Requirements

### 6.1 Performance
- Dashboard should load within 3 seconds
- AI chatbot should respond within 10 seconds for most queries
- Knowledge base search should return results within 2 seconds

### 6.2 Security & Compliance
- Must handle potentially sensitive competitive intelligence data
- No direct integration with student data (this tool analyzes requirements, not student records)
- Standard security practices for internal business tool
- Authentication required for all users

### 6.3 Scalability
- Initial scope: 50 US states
- Deep knowledge base for top 3 states (expandable)
- Potential future scope: International markets (if acquirer has global presence)

## 7. Technical Architecture

### 7.1 Current OnCourse Tech Stack (Context Only)

| Layer | Technology | Notes |
|-------|------------|-------|
| **Backend** | TBD (likely .NET or Java) | 25-year codebase |
| **Database** | Oracle Enterprise | Single-tenant; mature and scalable |
| **Frontend** | Sencha ExtJS | JavaScript framework for data-intensive apps |
| **Hosting** | Self-hosted / Managed Data Center | NOT cloud-native |
| **Security** | SOC 2 Type II | FERPA/COPPA compliant |
| **Integrations** | SIF, Ed-Fi, State APIs | Standards-compliant data exchange |
| **AI/ML** | None in production | Roadmap opportunities identified |

### 7.2 Expansion Planning Tool Architecture

**Key Decision**: This tool operates **independently** from the production SIS. It's a strategic planning application, not a transactional system.

**Recommended Stack**:

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | Python (FastAPI) | Strong AI/ML ecosystem; rapid development |
| **Database** | PostgreSQL | Relational data with JSON support |
| **Vector DB** | Pinecone / pgvector | Knowledge base embeddings for RAG |
| **LLM** | Claude (Anthropic) | Stakeholder preference |
| **Frontend** | React / Next.js | Modern web framework; data visualization |
| **Hosting** | Cloud (AWS/Azure/GCP) | Independent from OnCourse infrastructure |
| **Search** | Hybrid (semantic + keyword) | Best results for technical documentation |

### 7.3 AI Architecture

**RAG (Retrieval-Augmented Generation) Implementation**:
- Chunk state documentation appropriately for technical content
- Maintain source attribution for all content
- Implement version tracking for requirement changes
- Require citations in all AI responses
- Hybrid search (semantic + keyword) for best retrieval

**Grounding Requirements**:
- All AI responses must cite sources from knowledge base
- Confidence scoring for responses
- Clear indication when information may be outdated
- Comparison capabilities across states

## 8. UI/UX Requirements

### 8.1 Interface Approach

**Combination Interface**:
1. **Executive Dashboard**: State rankings with drill-down capability
2. **AI Chatbot**: Conversational interface for technical questions
3. **Report Generation**: PDF/PowerPoint for board/investor presentations

### 8.2 Dashboard Requirements

**State Rankings View**:
- Sortable/filterable list of all 50 states
- Composite score with factor breakdown
- Visual indicators (color coding by tier)
- Drill-down to detailed state profile
- Comparison view (side-by-side states)

**Gap Analysis View**:
- Visual representation of gaps vs. NJ/LA baseline
- Effort estimation breakdown
- Timeline projection
- Risk indicators

### 8.3 Output Formats

| Format | Use Case | Priority |
|--------|----------|----------|
| **Interactive Web Dashboard** | Day-to-day exploration and analysis | High |
| **PDF/PowerPoint Reports** | Board meetings, investor presentations, M&A materials | High |
| **Exportable Data (CSV/Excel)** | Custom analysis, spreadsheet modeling | Medium |

### 8.4 Chatbot Interface

**Design Principles**:
- Simple text input with conversation history
- Clear citation display for sources
- Ability to ask follow-up questions
- Export conversation to documentation
- Code snippet formatting for technical content

## 9. Integration Requirements

### 9.1 Required Integrations

| Integration | Purpose | Priority |
|-------------|---------|----------|
| State DOE websites | Primary data source for requirements | Critical |
| NCES data | District demographics, market sizing | Critical |
| CEDS standards | Common data element mappings | High |
| Claude API | LLM for AI chatbot | Critical |

### 9.2 Optional Integrations

| Integration | Purpose | Priority |
|-------------|---------|----------|
| OnCourse SIS | Capability baseline documentation (if accessible) | Low |
| CRM system | Competitive intel for sales team | Low |

## 10. Risks & Constraints

### 10.1 Known Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| **Timeline** | 1-3 months to show value | Prioritize MVP; iterative delivery |
| **No Existing Research** | Starting from scratch | Leverage AI for research acceleration |
| **Dev Team Focused on Core Product** | Limited internal capacity | Contractor/AI-assisted development |
| **Documentation Gap** | No consolidated field mappings | External DOE research; don't rely on internal docs |

### 10.2 Primary Concerns (from Stakeholder)

1. **Technical Feasibility**: Can we build this in 1-3 months?
2. **Data Quality/Availability**: Will state DOE data be consistent and accessible?

### 10.3 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| State DOE data inconsistency | High | Medium | AI-powered normalization; human review |
| Requirements change frequently | High | Medium | Version tracking; update monitoring |
| Competitive data hard to source | Medium | Medium | Multiple data sources; confidence scoring |
| AI hallucination on requirements | Medium | High | RAG grounding; citation requirements; validation |

### 10.4 Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Tool not ready before M&A milestone | Medium | High | Aggressive MVP scope; phased delivery |
| Rankings don't match reality | Medium | High | Validate against LA/NJ experience |
| Over-engineering vs. actual need | Medium | Medium | Start simple; iterate based on feedback |

## 11. Timeline & Milestones

### 11.1 Target Timeline: 1-3 Months

**Phase 1: Foundation (Weeks 1-4)**
- [ ] Set up infrastructure and development environment
- [ ] Build data collection pipeline for state DOE sources
- [ ] Create initial database schema
- [ ] Develop shallow analysis for all 50 states
- [ ] Build basic ranking algorithm

**Phase 2: Core Features (Weeks 5-8)**
- [ ] Refine ranking with development effort estimation
- [ ] Deep analysis for top 10 states
- [ ] Build executive dashboard
- [ ] Implement gap analysis module
- [ ] Validate rankings against NJ/LA experience

**Phase 3: AI Assistant (Weeks 9-12)**
- [ ] Build knowledge base for top 3 states
- [ ] Implement RAG architecture
- [ ] Deploy AI chatbot with Claude
- [ ] Add report generation (PDF/PowerPoint)
- [ ] User testing with dev team

### 11.2 MVP Definition

**Minimum Viable Product includes**:
1. ✅ State rankings for all 50 states (shallow analysis)
2. ✅ Gap analysis for top 3 states
3. ✅ Full knowledge base for top 3 states
4. ✅ AI chatbot for top 3 states (dev team use)
5. ✅ Executive dashboard
6. ✅ PDF/PowerPoint export

**Deferred to Post-MVP**:
- Competitive intelligence depth (beyond basic)
- Automated requirement change monitoring
- CRM integration
- Roadmap generator automation

## 12. Discovery Summary

### 12.1 Interview Completion Status

| Topic | Status | Key Findings |
|-------|--------|--------------|
| **Business Context** | ✅ Complete | 25-year company, M&A active, 1-3 month timeline |
| **Current Capabilities** | ✅ Complete | NJ/LA expertise, 2.5-3yr expansion timeline, 6x ARPU in LA |
| **Tech Stack** | ✅ Complete | Oracle/ExtJS (legacy), tool will be independent |
| **Ranking Criteria** | ✅ Complete | Development effort is PRIMARY factor |
| **UI/UX** | ✅ Complete | Dashboard + Chatbot + Reports combo |
| **AI/ML** | ✅ Complete | Claude, high trust, deep expert on chosen states |
| **Competitive Intel** | ✅ Complete | National + regional, all data types |
| **Timeline/Budget** | ✅ Complete | 1-3 months, no budget constraints |
| **Concerns** | ✅ Complete | Technical feasibility, data quality |

### 12.2 Critical Success Factors

1. **Development Effort Estimation**: Must accurately predict work required for new states
2. **Validation Against Experience**: Rankings must align with known NJ/LA reality
3. **AI Chatbot Depth**: Must be true expert on chosen states, not shallow generalist
4. **1-3 Month Delivery**: Must show value before M&A milestones
5. **Data Quality**: Must handle inconsistent state DOE documentation

### 12.3 Open Items for Development Planning

1. Confirm specific data thresholds for ranking validation
2. Identify initial data sources for each state DOE
3. Define exact competitive intelligence sources
4. Establish knowledge base content prioritization for top 3 states
5. Determine hosting environment (AWS vs Azure vs GCP)

---

## Appendix A: Company Profile

### OnCourse Systems for Education

| Attribute | Value |
|-----------|-------|
| **Founded** | Late 1990s (~25 years) |
| **Total Customers** | 254 K-12 educational organizations |
| **SIS Customers** | 115 districts |
| **ARR** | ~$7.6M |
| **Revenue Mix** | 95% recurring |
| **Avg Customer Tenure** | 9.4 years (69% retained 11+ years) |
| **EBITDA** | ~$1.3M |
| **Sales Staff** | 4 |
| **Development Team** | 8 engineers (10+ year avg tenure) |
| **Knowledge Management** | 9 staff |

### Geographic Footprint

| Market | Revenue Share | Customers | SIS Districts | Status |
|--------|---------------|-----------|---------------|--------|
| **New Jersey** | 60% | 176 | 104 | Home market |
| **Louisiana** | 37% | 26 | 9 parishes | Growth market (entered 2020) |
| **DC, Georgia** | 3% | 52 | 2 | Other |

### Key Metrics
- **NJ Average SIS ARPU**: ~$36K
- **LA Average SIS ARPU**: ~$220K (6x NJ)
- **Whitespace in Current Markets**: 632 districts (85%)
- **Competitive Loss Rate**: < $12K annual revenue to national competitors

### Louisiana Expansion Timeline (Benchmark)

| Phase | Duration |
|-------|----------|
| Market Research & Decision | ~6 months |
| LDOE Certification | ~12-18 months |
| First Sales Cycle | ~6-12 months |
| Implementation | ~6-12 months |
| **Total** | **~2.5-3 years** |

### ARPU Drivers (LA vs NJ)

| Factor | Contribution |
|--------|--------------|
| District Size (4-5x more students) | ~60% |
| Full Suite Adoption | ~25% |
| Pricing Maturity | ~10% |
| Implementation Services | ~5% |

---

## Appendix B: Technical Stakeholders

| Stakeholder | Role | Interest in Expansion Tool |
|-------------|------|---------------------------|
| Chris Contini | CEO | Strategic decisions; ROI justification |
| Mark Yelcick | CFO/CTO | Technical feasibility; budget approval |
| Diego Gallicchio | CIO | Infrastructure; data considerations |
| Joe Geary | Lead Systems Architect | Technical requirements; complexity estimation |
| Richard Gottlieb | Development Manager | Resource planning; implementation timeline |

---

## Appendix C: Product Portfolio

| Product | Revenue | % of Total | State Compliance Required |
|---------|---------|------------|---------------------------|
| SIS | $2.12M | 26.5% | Critical |
| Lesson Planner (Legacy) | $1.19M | 15% | None |
| Evaluate | $1.04M | 13% | Significant |
| Assessment | $915K | 11% | Moderate |
| Classroom (LMS) | $567K | 7% | None |
| Analytics | $315K | 4% | None |
| Data Manager | $303K | 4% | None |
| Curriculum Builder (Legacy) | $220K | 3% | None |
| MTSS | $101K | 1% | Moderate |

---

*Document Version: 1.0 - Discovery Complete*
*Last Updated: 2026-01-29*
*Next Step: Development planning and sprint definition*
