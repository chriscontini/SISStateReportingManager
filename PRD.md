# Product Requirements Document (PRD)
# SISStateReportingManager

**Version**: 0.3 (Draft)
**Last Updated**: 2026-01-29
**Status**: Discovery Phase - Requirements Gathering

---

## 1. Executive Summary

SISStateReportingManager is an AI-powered strategic expansion planning tool for **OnCourse Systems for Education**, a 25-year-old K-12 EdTech SaaS company. The application will help OnCourse identify and prioritize new state markets for SIS expansion by analyzing state reporting requirements, competitive landscapes, and alignment with existing capabilities.

**Key Business Context**:
- OnCourse serves 254 K-12 educational organizations (115 SIS customers)
- Current ARR: ~$7.6M with 95% recurring revenue
- Geographic concentration: NJ (60%), LA (37%), DC/GA (3%)
- Active M&A process creates urgency for demonstrating credible expansion roadmap
- Louisiana expansion model (6x ARPU vs NJ) proves geographic expansion value

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

| User Role | Primary Use Case | Frequency |
|-----------|------------------|-----------|
| **Executive Leadership** (CEO, Partners) | Strategic state prioritization; M&A geographic synergies; investor discussions on growth runway | Weekly/Monthly |
| **Product Management** | Roadmap planning for state compliance modules; feature prioritization by market size | Weekly |
| **Development Team** | Implementation guidance on state requirements; engineering effort estimation | Per-project |
| **Sales Team** | Competitive positioning; target district identification; incumbent vendor analysis | Daily |

**Primary User**: Executive leadership for strategic planning, with cascading benefits to product and sales teams.

## 3. Product Vision & Goals

### 3.1 Vision Statement

Enable OnCourse to make data-driven state expansion decisions by providing comprehensive intelligence on state reporting requirements, competitive landscapes, and development effort—transforming a 2-3 year research process into weeks.

### 3.2 Success Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| **State Analysis Time** | < 2 weeks per state (vs. months) | Accelerate expansion planning |
| **Expansion Decision Confidence** | Quantified scoring for all 50 states | Remove gut-feel from strategic decisions |
| **Development Estimation Accuracy** | Gap analysis within 20% of actual effort | Better resource planning |
| **M&A Readiness** | Documented expansion roadmap for top 3-5 states | Support valuation discussions |
| **Louisiana-like Opportunity Identification** | Identify states with similar ARPU potential | Replicate 6x ARPU success |

### 3.3 Strategic Context

**M&A Timeline Consideration**: OnCourse is preparing for potential transaction with PE or strategic buyers. Key value drivers:
- Demonstrating credible multi-state expansion roadmap impacts valuation
- Revenue multiple arbitrage between regional ($X) and national ($X+) platforms
- Capital deployment plan ready for Day 1 post-close

## 4. User Personas

### 4.1 Strategic Decision Maker (Primary)
- **Role**: CEO / Managing Partner (Chris Contini)
- **Goals**: Identify highest-ROI expansion states; build investor-ready growth story
- **Pain Points**: Lack of data-driven framework; time constraints; risk of wrong state choice
- **Success Criteria**: Confident, defensible expansion recommendations with clear rationale

### 4.2 Technical/Financial Leader
- **Role**: CFO/CTO (Mark Yelcick)
- **Goals**: Assess technical feasibility; approve budget; validate ROI assumptions
- **Pain Points**: Unknown development costs for new states; infrastructure implications
- **Success Criteria**: Clear cost estimates; technical risk assessment

### 4.3 Infrastructure Leader
- **Role**: CIO (Diego Gallicchio)
- **Goals**: Understand infrastructure implications; plan data architecture
- **Pain Points**: Scaling considerations; data management complexity
- **Success Criteria**: Infrastructure requirements documented; integration path clear

### 4.4 Technical Architect
- **Role**: Lead Systems Architect (Joe Geary)
- **Goals**: Estimate complexity; plan technical implementation
- **Pain Points**: Scattered state specs; unknown integration requirements
- **Success Criteria**: Comprehensive technical requirements; AI assistant for ongoing questions

## 5. Functional Requirements

### 5.1 State Requirements Research Engine

**Purpose**: Aggregate and analyze K-12 state reporting requirements across all 50 states.

**Key Insight from Discovery**: OnCourse's field mappings exist in code but there's no consolidated external dictionary. The tool must research new state requirements from external DOE sources, not rely on pre-built mappings.

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

**Ranking Factors** (refined from discovery):

| Factor | Weight | Description | Data Source |
|--------|--------|-------------|-------------|
| **District Structure** | High | Parish/county model (like LA) vs fragmented districts (like NJ) | NCES data |
| **Average District Size** | High | Larger districts = higher ARPU potential | NCES data |
| **Technical Fit** | High | How closely existing NJ/LA code matches state requirements | DOE documentation |
| **Certification Complexity** | Medium | Formal vendor certification vs. open market | DOE documentation |
| **Competitive Landscape** | Medium | Density of established competitors | Market research |
| **Market Opportunity** | Medium | Total addressable market; growth potential | NCES data |
| **Regulatory Complexity** | Medium | Compliance burden beyond core reporting | DOE documentation |
| **Geographic Proximity** | Low | Ease of support and relationship building | Geography |

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
- Comparison views across states

### 5.7 AI Development Assistant

**Purpose**: Support the development team with AI-powered Q&A about state requirements.

**Capabilities**:
- Answer questions about state-specific requirements
- Explain data element definitions and mappings
- Compare requirements across states (NJ vs LA vs target)
- Provide implementation guidance based on LA experience
- Track new/changed requirements
- Surface relevant knowledge base content

**Key Use Case**: Help the 8-person dev team (10+ year average tenure) leverage their NJ/LA expertise when evaluating new states.

### 5.8 Competitive Intelligence Module

**Purpose**: Analyze competitive landscape in target states.

**Analysis Areas**:
- National SIS vendors present (PowerSchool, Infinite Campus, etc.)
- Regional competitors and market share
- Vendor strengths and weaknesses
- Customer satisfaction indicators
- Contract renewal cycles (where discoverable)
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
*To be defined*

### 6.2 Security & Compliance
- Must handle potentially sensitive competitive intelligence data
- No direct integration with student data (this tool analyzes requirements, not student records)
- Standard security practices for internal business tool

### 6.3 Scalability
- Initial scope: 50 US states
- Potential future scope: International markets (if acquirer has global presence)

## 7. Technical Architecture

### 7.1 Current OnCourse Tech Stack (Context)

| Layer | Technology | Notes |
|-------|------------|-------|
| **Backend** | TBD (likely .NET or Java) | 25-year codebase |
| **Database** | Oracle Enterprise | Single-tenant; mature and scalable |
| **Frontend** | Sencha ExtJS | JavaScript framework for data-intensive apps |
| **Hosting** | Self-hosted / Managed Data Center | NOT cloud-native |
| **Security** | SOC 2 Type II | FERPA/COPPA compliant |
| **Integrations** | SIF, Ed-Fi, State APIs | Standards-compliant data exchange |
| **AI/ML** | None in production | Roadmap opportunities identified |

### 7.2 Expansion Planning Tool Architecture (TBD)

**Key Decision**: This tool operates independently from the production SIS. It's a strategic planning application, not a transactional system.

**Recommended Approach** (to be validated):
- Modern cloud-native architecture (AWS/Azure/GCP)
- Python backend for AI/ML capabilities
- Vector database for knowledge base (RAG)
- React/Next.js frontend for data visualization
- Independent from Oracle/Sencha stack

## 8. UI/UX Requirements

*To be defined in Interview Part 3*

## 9. Integration Requirements

### 9.1 Required Integrations
- State DOE websites (web scraping/research)
- NCES (National Center for Education Statistics) data
- CEDS standards documentation
- Competitive intelligence sources

### 9.2 Optional Integrations
- OnCourse SIS (for capability baseline documentation)
- CRM system (for sales team competitive intel)

## 10. Risks & Constraints

### 10.1 Known Constraints
- **Budget**: Bootstrap operation with ~$1.3M EBITDA; internal tool investment initially
- **Timeline**: M&A process creates urgency for demonstrable progress
- **Resources**: 8-person dev team focused on core product; limited capacity for new tool
- **Documentation Gap**: Field mappings exist in code but no consolidated external dictionary

### 10.2 Technical Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| State DOE data inconsistency | High | Medium | AI-powered normalization; human review |
| Requirements change frequently | High | Medium | Version tracking; update monitoring |
| Competitive data hard to source | Medium | Medium | Multiple data sources; confidence scoring |
| AI hallucination on requirements | Medium | High | RAG grounding; citation requirements |

### 10.3 Business Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Tool not ready before M&A close | Medium | High | Prioritize MVP for top 5-10 states |
| Rankings don't match reality | Medium | High | Validate against LA experience |
| Over-engineering vs. actual need | Medium | Medium | Start simple; iterate based on use |

## 11. Timeline & Milestones

*To be defined in Interview Part 4*

## 12. Open Questions

### Captured During Discovery

**Part 1 - Business Context** ✅
- [x] Company profile and current state
- [x] Pain points and challenges
- [x] User roles and use cases
- [x] Urgency drivers
- [x] Commercial intent

**Part 2 - Current Capabilities** ✅
- [x] NJ state reporting (NJSLEDS transition, 104 districts, 20+ years)
- [x] LA state reporting (EdLink, 9 parishes, 6x ARPU, 2.5-3yr timeline)
- [x] Tech stack (Oracle, Sencha ExtJS, self-hosted, no AI/ML)
- [x] Development team (8 engineers, 10+ year tenure)
- [x] Product portfolio (Hub & Spoke model, state compliance requirements)

**Part 3 - Remaining Topics** (Next)
- [ ] State ranking criteria weights and preferences
- [ ] UI/UX requirements and workflows
- [ ] Data sources and research approach
- [ ] AI/ML implementation preferences
- [ ] Competitive intelligence requirements
- [ ] Timeline and budget constraints
- [ ] MVP vs. full product scope

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

*This document will be updated iteratively during the discovery process.*
