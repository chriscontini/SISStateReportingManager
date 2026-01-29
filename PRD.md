# Product Requirements Document (PRD)
# SISStateReportingManager

**Version**: 0.2 (Draft)
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
- **Role**: CEO / Managing Partner
- **Goals**: Identify highest-ROI expansion states; build investor-ready growth story
- **Pain Points**: Lack of data-driven framework; time constraints; risk of wrong state choice
- **Success Criteria**: Confident, defensible expansion recommendations with clear rationale

### 4.2 Product Leader
- **Role**: VP Product / Product Manager
- **Goals**: Plan multi-year compliance module roadmap; prioritize features by market opportunity
- **Pain Points**: Unknown scope of state requirements; unclear feature overlap
- **Success Criteria**: Detailed gap analysis with effort estimates; clear build sequence

### 4.3 Technical Leader
- **Role**: VP Engineering / Tech Lead
- **Goals**: Understand technical requirements for new states; estimate development resources
- **Pain Points**: State reporting specs are scattered/inconsistent; unknown integration requirements
- **Success Criteria**: Comprehensive technical requirements; AI assistant for ongoing questions

### 4.4 Sales Leader
- **Role**: VP Sales / Sales Manager
- **Goals**: Target right districts; understand competitive positioning; build pipeline
- **Pain Points**: No visibility into competitor installed base; manual prospect research
- **Success Criteria**: Actionable competitive intelligence; target district lists

## 5. Functional Requirements

### 5.1 State Requirements Research Engine
*To be defined - see Interview Part 2*

### 5.2 Capability Matching System
*To be defined - see Interview Part 2*

### 5.3 State Ranking Engine
*To be defined - see Interview Part 3*

### 5.4 Gap Analysis Module
*To be defined - see Interview Part 3*

### 5.5 Roadmap Generator
*To be defined - see Interview Part 4*

### 5.6 Knowledge Base Builder
*To be defined - see Interview Part 5*

### 5.7 AI Development Assistant
*To be defined - see Interview Part 5*

### 5.8 Competitive Intelligence Module
*To be defined - see Interview Part 6*

### 5.9 Product Alignment Analyzer
*To be defined - see Interview Part 6*

## 6. Non-Functional Requirements

### 6.1 Performance
*To be defined*

### 6.2 Security & Compliance
*To be defined*

### 6.3 Scalability
*To be defined*

## 7. Technical Architecture

*To be defined*

## 8. UI/UX Requirements

*To be defined*

## 9. Integration Requirements

*To be defined*

## 10. Risks & Constraints

### 10.1 Known Constraints
- **Budget**: Bootstrap operation with ~$1.3M EBITDA; internal tool investment initially
- **Timeline**: M&A process creates urgency for demonstrable progress
- **Resources**: Limited internal technical capacity for new tool development

### 10.2 Risks
*To be identified during discovery*

## 11. Timeline & Milestones

*To be defined*

## 12. Open Questions

### Captured During Discovery

**Part 1 - Business Context** (Completed)
- [x] Company profile and current state
- [x] Pain points and challenges
- [x] User roles and use cases
- [x] Urgency drivers
- [x] Commercial intent

**Part 2 - Current Capabilities** (Next)
- [ ] Current state reporting implementations (NJ, LA specifics)
- [ ] Existing data models and schemas
- [ ] Technical architecture of current SIS
- [ ] Documentation of current capabilities

**Part 3+ - Remaining Topics**
- [ ] Technical preferences and constraints
- [ ] UI/UX requirements
- [ ] Data sources and integrations
- [ ] AI/ML implementation details
- [ ] Competitive intelligence needs
- [ ] Timeline and budget details

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

---

*This document will be updated iteratively during the discovery process.*
