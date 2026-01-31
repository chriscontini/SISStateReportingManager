"""
Seed knowledge articles for target states (PA, TX, MD).

This script creates comprehensive knowledge articles about state
reporting requirements, certification processes, and integration details.
"""

import asyncio
from sqlalchemy import select

from .database import get_engine, get_session_maker
from .models import State, KnowledgeArticle
from .services.knowledge_service import KnowledgeService


# Knowledge articles for Pennsylvania
PA_ARTICLES = [
    {
        "title": "PIMS (Pennsylvania Information Management System) Overview",
        "category": "reporting",
        "content": """# PIMS Overview

The Pennsylvania Information Management System (PIMS) is Pennsylvania's statewide longitudinal data system that collects, stores, and reports education data.

## Key Collections

1. **Student Data** - Demographics, enrollment, attendance
2. **Staff Data** - Certification, assignments, compensation
3. **Course Data** - Offerings, enrollment, grades
4. **Assessment Data** - PSSA, Keystone, ACCESS

## Submission Windows

- **October Snapshot** (Child Accounting)
- **December Submission** (End of First Semester)
- **June Submission** (End of Year)
- **Summer Submission** (July-August corrections)

## Data Quality Requirements

- All fields validated against PA data dictionary
- LEA-level certification required
- Error resolution within 10 business days

## Resources

- PDE Data Quality Office
- PIMS User Manual (updated annually)
- Technical Assistance webinars""",
        "source_url": "https://www.education.pa.gov/DataAndReporting/PIMS/Pages/default.aspx",
        "tags": ["PIMS", "data collection", "PDE", "reporting system"],
    },
    {
        "title": "Pennsylvania Keystone Exams Integration",
        "category": "assessment",
        "content": """# Keystone Exams Integration Guide

The Keystone Exams are Pennsylvania's end-of-course assessments in Algebra I, Literature, and Biology.

## Integration Requirements

### Data Elements
- Student demographics (match to PIMS)
- Course enrollment records
- Assessment accommodations
- Test administration data

### File Formats
- Pre-ID files for student registration
- Score import files (CSV)
- Demographic updates

## Act 158 Graduation Pathways

As of Act 158, students can meet graduation requirements through:
1. Keystone proficiency
2. Alternative assessments
3. Career-ready pathways
4. Evidence-based demonstrations

## Implementation Notes

- Sync student data 2 weeks before testing windows
- Handle mid-year transfers with care
- Track retake eligibility automatically
- Support IEP/504 accommodation flags""",
        "source_url": "https://www.education.pa.gov/K-12/Assessment and Accountability/Keystone Exams/Pages/default.aspx",
        "tags": ["Keystone", "assessment", "Act 158", "graduation"],
    },
    {
        "title": "Pennsylvania Safe Schools Reporting",
        "category": "reporting",
        "content": """# Safe Schools Reporting (Act 26)

Pennsylvania requires all schools to report incidents under Act 26 Safe Schools regulations.

## Reportable Incidents

- Weapons possession
- Drug and alcohol offenses
- Violence against students/staff
- Bullying incidents
- Criminal acts on school property

## Data Elements

| Field | Description | Required |
|-------|-------------|----------|
| Incident Type | Category code | Yes |
| Date/Time | When occurred | Yes |
| Location | School building code | Yes |
| Persons Involved | Student/Staff IDs | Yes |
| Resolution | Actions taken | Yes |

## Submission Timeline

- Real-time entry preferred
- End-of-year summary required
- July 31 deadline for prior year

## Integration Points

- Student discipline module
- Incident tracking system
- Staff notification system""",
        "source_url": "https://www.education.pa.gov/Schools/safeschools/Pages/default.aspx",
        "tags": ["safe schools", "Act 26", "discipline", "incidents"],
    },
    {
        "title": "Pennsylvania Special Education Reporting",
        "category": "special_education",
        "content": """# Special Education Data Reporting

Pennsylvania special education data flows through PIMS with specific requirements for IEP students.

## Key Data Collections

### Child Count (December 1)
- All students with active IEPs
- Primary and secondary disability codes
- Educational environment codes
- Services delivered

### Exit Data
- Graduation status
- Exit reasons
- Outcome data

## BSE (Bureau of Special Education) Requirements

1. **IEP Timelines** - Tracked for compliance
2. **LRE Calculations** - Time in regular education
3. **Transition Planning** - Age 14+ requirements
4. **Progress Monitoring** - Annual goal tracking

## Data Quality Checks

- PAUN (Unique Student ID) validation
- Disability code verification
- Service minutes reconciliation
- Provider qualification verification

## Integration Needs

- IEP management system sync
- Medicaid billing data export
- Parent notification tracking""",
        "source_url": "https://www.education.pa.gov/K-12/Special Education/Pages/default.aspx",
        "tags": ["special education", "IEP", "BSE", "child count"],
    },
    {
        "title": "PIMS Technical Specifications",
        "category": "integration",
        "content": """# PIMS Technical Integration Guide

Technical specifications for integrating with Pennsylvania's PIMS system.

## File Specifications

### Format
- Fixed-width text files
- UTF-8 encoding
- CRLF line endings

### Templates
Each template has specific field positions:
- Student Template (65+ fields)
- Staff Template (40+ fields)
- Course Template (30+ fields)

## Validation Rules

```
Field: AUN (9 digits)
Format: XXXXXXXXX
Validation: Must exist in PDE directory

Field: PASECUREID (10 digits)
Format: XXXXXXXXXX
Validation: Must be unique, check digit required
```

## API Options

- SFTP upload to PDE servers
- Batch validation service
- Error report retrieval

## Security Requirements

- TLS 1.2+ for all transfers
- LEA-level user authentication
- Audit logging required

## Error Handling

1. Pre-submission validation
2. Batch error reports (24-48 hours)
3. Individual record correction
4. Re-submission process""",
        "source_url": "https://www.education.pa.gov/DataAndReporting/PIMS/Resources/Pages/default.aspx",
        "tags": ["technical", "integration", "API", "file format"],
    },
]

# Knowledge articles for Texas
TX_ARTICLES = [
    {
        "title": "PEIMS (Public Education Information Management System) Overview",
        "category": "reporting",
        "content": """# PEIMS Overview

The Public Education Information Management System is Texas's statewide data collection system managed by the Texas Education Agency (TEA).

## Submission Windows

1. **Fall Submission** (October)
   - Student enrollment
   - Staff data
   - Organization data

2. **Mid-Year Submission** (January)
   - Attendance updates
   - Program participation

3. **Summer Submission** (June)
   - End of year data
   - Graduate tracking
   - Assessment results

4. **Extended Year** (August)
   - Final corrections
   - Resubmissions

## Data Standards

- TSDS (Texas Student Data System) format
- Ed-Fi aligned data model
- Real-time validation available

## Key Reports Generated

- Academic Excellence Indicator System (AEIS)
- TAPR (Texas Academic Performance Reports)
- Accountability ratings""",
        "source_url": "https://tea.texas.gov/reports-and-data/data-submission/peims",
        "tags": ["PEIMS", "TEA", "data collection", "TSDS"],
    },
    {
        "title": "TSDS (Texas Student Data System) Integration",
        "category": "integration",
        "content": """# TSDS Integration Guide

TSDS is Texas's Ed-Fi-based platform for real-time data exchange.

## Architecture

```
SIS → TSDS Core → PEIMS
         ↓
    Data Portal
         ↓
    TEA Reports
```

## API Specifications

- RESTful Ed-Fi API
- OAuth 2.0 authentication
- JSON data format
- Real-time validation

## Data Domains

1. **Student Domain**
   - Demographics
   - Enrollment
   - Programs

2. **Staff Domain**
   - Credentials
   - Assignments
   - Evaluations

3. **Education Organization**
   - Schools
   - Districts
   - Charters

## Certification Requirements

- Vendor must pass TSDS certification
- Annual recertification required
- Compliance testing environment provided

## Best Practices

- Use staging environment first
- Implement error retry logic
- Monitor API rate limits
- Cache authentication tokens""",
        "source_url": "https://www.texasstudentdatasystem.org/",
        "tags": ["TSDS", "Ed-Fi", "API", "integration"],
    },
    {
        "title": "STAAR Assessment Data Integration",
        "category": "assessment",
        "content": """# STAAR Assessment Integration

State of Texas Assessments of Academic Readiness (STAAR) data integration requirements.

## Assessment Types

- STAAR Grades 3-8 (Reading, Math, Science, Social Studies)
- STAAR End-of-Course (Algebra I, English I/II, Biology, US History)
- STAAR Alternate 2 (for students with significant cognitive disabilities)

## Pre-Administration

### Student Pre-ID Files
- Demographic data sync
- Accommodation flags
- Testing eligibility

### Key Fields
- PEIMS ID (unique identifier)
- Grade level
- Program participation
- LEP status
- Special education status

## Post-Administration

### Score Import
- Scale scores
- Performance levels
- Progress measures

### Reporting
- Individual student reports
- Campus/district summaries
- A-F accountability data

## Timeline

| Activity | Window |
|----------|--------|
| Pre-ID submission | 4 weeks before testing |
| Answer documents | 2 weeks before testing |
| Score release | 6-8 weeks after testing |""",
        "source_url": "https://tea.texas.gov/student-assessment/testing/staar",
        "tags": ["STAAR", "assessment", "accountability", "scores"],
    },
    {
        "title": "Texas Certification Requirements for SIS Vendors",
        "category": "certification",
        "content": """# TEA Vendor Certification

Texas Education Agency certification requirements for Student Information System vendors.

## Certification Process

### Phase 1: Application
- Company profile submission
- Product documentation
- Reference customers

### Phase 2: Technical Review
- TSDS integration testing
- PEIMS export validation
- Security assessment

### Phase 3: Pilot Testing
- 2-3 pilot districts
- Full submission cycle
- Error resolution tracking

### Phase 4: Certification
- Official TEA approval
- Vendor portal access
- Support channel activation

## Ongoing Requirements

1. **Annual Recertification**
   - Updated compliance testing
   - New data element support
   - Security audit

2. **Change Notifications**
   - Major version changes
   - Data model updates
   - Security incidents

3. **Support Standards**
   - Response time SLAs
   - Escalation procedures
   - Training availability

## Estimated Timeline

- Initial certification: 6-12 months
- Annual recertification: 2-3 months
- Major update certification: 3-6 months""",
        "source_url": "https://tea.texas.gov/reports-and-data/data-submission",
        "tags": ["certification", "TEA", "compliance", "vendor"],
    },
    {
        "title": "Texas Special Programs Reporting",
        "category": "reporting",
        "content": """# Special Programs Reporting in PEIMS

Texas requires detailed reporting for various special programs through PEIMS.

## Bilingual/ESL Programs

- Language proficiency data
- Program type codes
- LPAC decisions
- Exit criteria tracking

## Special Education

- Disability codes (TEA-specific)
- Instructional setting codes
- Related services
- ARD/IEP data elements

## Career and Technical Education (CTE)

- CTE course sequences
- Industry certifications
- Work-based learning hours
- Completer status

## Gifted and Talented

- Identification data
- Services provided
- Program participation

## At-Risk Students

- At-risk indicator criteria (13 categories)
- Intervention programs
- Progress tracking

## Data Validation

Each program has specific cross-validation rules:
- Enrollment × Services
- Demographics × Program eligibility
- Course enrollment × Program participation""",
        "source_url": "https://tea.texas.gov/reports-and-data/data-submission/peims/peims-standards",
        "tags": ["special programs", "bilingual", "special education", "CTE"],
    },
]

# Knowledge articles for Maryland
MD_ARTICLES = [
    {
        "title": "Maryland MSDE Data Collection Overview",
        "category": "reporting",
        "content": """# MSDE Data Collection Overview

Maryland State Department of Education data collection operates through a county-based system with 24 local education agencies (LEAs).

## Structure

Maryland has 24 LEAs:
- 23 county public school systems
- Baltimore City Public Schools

This county-based model (similar to Louisiana parishes) simplifies data collection compared to states with fragmented districts.

## Key Collections

### Student Data
- Enrollment (Fall, Spring counts)
- Attendance
- Demographics
- Program participation

### Staff Data
- Certifications
- Assignments
- Highly qualified status

### Finance Data
- Expenditures
- Revenue sources
- Per-pupil costs

## Submission Calendar

| Collection | Deadline |
|------------|----------|
| Fall Enrollment | October 15 |
| Staff Data | November 1 |
| December Child Count | December 15 |
| Spring Enrollment | April 1 |
| End of Year | July 1 |""",
        "source_url": "https://www.marylandpublicschools.org/about/Pages/DCAA/index.aspx",
        "tags": ["MSDE", "data collection", "county model", "LEA"],
    },
    {
        "title": "MCAP Assessment Integration",
        "category": "assessment",
        "content": """# MCAP Assessment Data Integration

Maryland Comprehensive Assessment Program (MCAP) integration requirements.

## Assessment Components

1. **MCAP English Language Arts** (Grades 3-8, 10)
2. **MCAP Mathematics** (Grades 3-8, Algebra I, Geometry)
3. **MISA** (Maryland Integrated Science Assessment)
4. **Social Studies** (End of Course)

## Data Requirements

### Pre-Administration
- Student demographics sync
- Accommodation flags (IEP/504)
- Testing eligibility verification
- Test administrator assignments

### Post-Administration
- Score import (scale scores, performance levels)
- Growth measures
- Subgroup reporting data

## Timeline

- **Registration window**: 6 weeks before testing
- **Pre-ID verification**: 2 weeks before testing
- **Score release**: 6-8 weeks after testing

## Integration Points

```
SIS → Pre-ID Export → Testing Platform
                           ↓
SIS ← Score Import ← Results Files
```

## File Formats

- CSV exports for registration
- XML or CSV for score imports
- Standard demographic codes""",
        "source_url": "https://www.marylandpublicschools.org/about/Pages/DAAIT/Assessment/index.aspx",
        "tags": ["MCAP", "assessment", "testing", "scores"],
    },
    {
        "title": "Maryland Bridge Plan for Academic Validation",
        "category": "reporting",
        "content": """# Bridge Plan for Academic Validation

Maryland's Bridge Plan provides alternative pathways to demonstrate readiness for graduation.

## Overview

Students who do not meet MCAP proficiency requirements can demonstrate readiness through the Bridge Plan.

## Bridge Plan Options

1. **Portfolio Assessment**
   - Collection of student work
   - Rubric-based evaluation
   - Teacher validation

2. **Alternative Assessments**
   - SAT/ACT scores
   - AP exam scores
   - IB assessments
   - Career certifications

3. **Course Performance**
   - Grades in related courses
   - GPA requirements
   - Credit completion

## Data Tracking Requirements

### Per Student
- MCAP scores (baseline)
- Bridge Plan selection
- Evidence documentation
- Completion status

### Reporting
- Aggregate Bridge Plan usage
- Pathway distribution
- Completion rates by demographic

## Implementation Notes

- Track timeline for completion
- Document validation signatures
- Store portfolio artifacts (links)
- Report Bridge Plan status in student records""",
        "source_url": "https://www.marylandpublicschools.org/about/Pages/DAAIT/Assessment/BridgePlan/index.aspx",
        "tags": ["Bridge Plan", "graduation", "alternative assessment", "pathways"],
    },
    {
        "title": "Maryland Special Education (IDEA) Reporting",
        "category": "special_education",
        "content": """# Maryland IDEA Special Education Reporting

Maryland special education data collection requirements under IDEA.

## Key Collections

### December 1 Child Count
- All students with active IEPs
- Primary disability categories
- Educational environment (LRE)
- Age/grade distribution

### Annual Performance Report
- Indicator data (20 indicators)
- Dispute resolution data
- Transition outcomes

## Disability Categories

Maryland uses federal IDEA categories:
- Autism
- Deaf-Blindness
- Developmental Delay
- Emotional Disability
- Hearing Impairment
- Intellectual Disability
- Multiple Disabilities
- Orthopedic Impairment
- Other Health Impairment
- Specific Learning Disability
- Speech/Language Impairment
- Traumatic Brain Injury
- Visual Impairment

## IEP Data Elements

- Service minutes by type
- Provider assignments
- Goal progress data
- Parent participation
- Meeting compliance

## Integration Requirements

- IEP system sync
- Service tracking
- Compliance monitoring
- Medicaid billing export""",
        "source_url": "https://www.marylandpublicschools.org/programs/Pages/Special-Education/index.aspx",
        "tags": ["special education", "IDEA", "IEP", "child count"],
    },
    {
        "title": "Maryland County-Based Implementation Strategy",
        "category": "implementation",
        "content": """# County-Based Implementation Strategy for Maryland

Strategic approach to implementing in Maryland's county-based system.

## Why Maryland is Favorable

1. **Only 24 LEAs** - Simplified sales and implementation
2. **County Model** - Similar to Louisiana parish success
3. **Larger Districts** - Higher ARPU per customer
4. **Unified Requirements** - Consistent MSDE standards

## Implementation Approach

### Phase 1: Initial Counties (6 months)
- Target 2-3 mid-size counties
- Build MSDE compliance
- Establish references

### Phase 2: Expansion (6-12 months)
- Leverage success stories
- Target larger counties
- Build support infrastructure

### Phase 3: Statewide (12-24 months)
- State contract consideration
- Full coverage capability
- Regional support team

## Key Success Factors

1. **MSDE Relationships**
   - Early engagement
   - Compliance partnership
   - Technical consultation

2. **Reference Counties**
   - Frederick County (moderate size)
   - Howard County (high performing)
   - Baltimore County (large urban)

3. **Support Model**
   - Regional specialists
   - MSDE liaison
   - Training programs

## LA Lessons Applied

From Louisiana expansion:
- County/parish model reduces complexity
- Single state standard simplifies compliance
- Larger customers = better economics""",
        "source_url": "https://www.marylandpublicschools.org/",
        "tags": ["implementation", "strategy", "county model", "expansion"],
    },
]


async def seed_knowledge_articles():
    """Seed knowledge articles for target states."""
    engine = get_engine()
    SessionLocal = get_session_maker(engine)

    async with SessionLocal() as session:
        service = KnowledgeService(session)

        print("=" * 60)
        print("SEEDING KNOWLEDGE ARTICLES")
        print("=" * 60)

        # Get state IDs
        states_map = {}
        for abbrev in ["PA", "TX", "MD"]:
            result = await session.execute(
                select(State).where(State.abbreviation == abbrev)
            )
            state = result.scalar_one_or_none()
            if state:
                states_map[abbrev] = state.id
                print(f"Found {abbrev}: ID {state.id}")
            else:
                print(f"WARNING: State {abbrev} not found!")

        # Check for existing articles
        existing = await session.execute(
            select(KnowledgeArticle)
        )
        existing_count = len(list(existing.scalars().all()))

        if existing_count > 0:
            print(f"\nFound {existing_count} existing articles. Skipping seed.")
            print("Delete existing articles to re-seed.")
            return

        articles_data = [
            ("PA", PA_ARTICLES),
            ("TX", TX_ARTICLES),
            ("MD", MD_ARTICLES),
        ]

        total_created = 0
        for abbrev, articles in articles_data:
            if abbrev not in states_map:
                continue

            state_id = states_map[abbrev]
            print(f"\n--- Creating articles for {abbrev} ---")

            for article_data in articles:
                article = await service.create_article(
                    state_id=state_id,
                    title=article_data["title"],
                    content=article_data["content"],
                    category=article_data["category"],
                    source_url=article_data.get("source_url"),
                    tags=article_data.get("tags", []),
                )
                print(f"  Created: {article.title[:50]}...")
                total_created += 1

        print(f"\n{'=' * 60}")
        print(f"CREATED {total_created} KNOWLEDGE ARTICLES")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(seed_knowledge_articles())
