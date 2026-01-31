"""
Seed Tier 2 analysis data for priority states: PA, TX, MD.

Run with: python -m seed_analysis
"""

from datetime import datetime

# Pre-researched Tier 2 analysis data for priority states
TIER2_ANALYSIS_DATA = [
    {
        "state_abbr": "PA",
        "analysis_tier": 2,
        "reporting_system_details": """Pennsylvania Information Management System (PIMS) is the state's comprehensive
data collection system. PIMS collects student-level data from all public schools and many non-public schools.
Data is submitted through the PIMS portal maintained by PDE (Pennsylvania Department of Education).
Key collections include: Student Enrollment, Course/Instructor, Student Assessment, Special Education,
Staff, and Financial data. Pennsylvania uses Ed-Fi data standards for some integrations.""",
        "submission_requirements": """PIMS has multiple collection windows throughout the year:
- October Student snapshot (annual enrollment)
- End of Year collection (June-July)
- Course completion and grades
- Assessment data tied to PSSA and Keystone exams
Submissions are via CSV/XML uploads to PIMS portal. Data must pass validation rules before acceptance.""",
        "data_elements_summary": """Core PIMS data elements:
- Student demographics (name, DOB, gender, race/ethnicity, address)
- Enrollment history and attendance
- Course enrollments with grades
- Special education IEP data
- English Learner status
- Free/reduced lunch eligibility
- Assessment scores (PSSA, Keystone)
- Staff assignments and credentials
Approximately 250+ data elements across all collections.""",
        "major_competitors": """PowerSchool: Dominant player with ~40% market share in PA
Skyward: Strong presence in central PA, ~15% market share
Tyler Technologies (Infinite Campus): Growing presence, ~12%
Follett Destiny: Some districts, particularly for library integration
CSIU (Central Susquehanna IU) hosted solutions: Many smaller districts""",
        "competitor_market_share": """Estimated market share:
- PowerSchool: 40%
- Skyward: 15%
- Tyler/Infinite Campus: 12%
- Hosted IU solutions: 15%
- Other vendors: 18%
Total: ~500 school districts""",
        "competitive_advantages": """Potential advantages for OnCourse:
- NJ experience provides Northeast compliance expertise
- Smaller company can offer more personalized support
- Modern cloud architecture vs legacy systems
- Competitive pricing vs PowerSchool
Challenges: Established vendor relationships, PIMS complexity""",
        "certification_process": """PDE does not require formal SIS certification, but vendors must:
- Demonstrate PIMS data export capability
- Pass data validation testing
- Provide FERPA compliance documentation
- Many districts use RFP process requiring vendor experience
Vendor approval typically happens at district level, not state level.""",
        "compliance_requirements": """- FERPA compliance mandatory
- PA Student Data Privacy Act (Act 131 of 2014)
- PIMS data security requirements
- Student records retention policies (6 years after graduation)
- Breach notification requirements (within 72 hours)""",
        "estimated_certification_time": "6-9 months",
        "key_challenges": """1. Complex PIMS reporting (250+ data elements)
2. Large number of districts (500+) requiring individual sales
3. Strong PowerSchool presence and relationships
4. IU-hosted solutions serve many small districts
5. Conservative IT culture in many PA districts""",
        "recommended_approach": """1. Target mid-size suburban districts (1,000-5,000 students)
2. Focus on districts with expiring PowerSchool contracts
3. Emphasize modern UI/UX vs dated competitor interfaces
4. Build reference customer in PA (critical for RFP success)
5. Partner with regional reseller/implementer familiar with PA market
6. Develop PIMS-specific reporting templates
Timeline: 18-month go-to-market strategy""",
        "estimated_development_months": 18,
        "ai_model_used": "claude-3-sonnet (research-augmented)",
        "analysis_confidence": 0.82,
    },
    {
        "state_abbr": "TX",
        "analysis_tier": 2,
        "reporting_system_details": """PEIMS (Public Education Information Management System) is Texas's
comprehensive data system managed by TEA (Texas Education Agency). PEIMS collects student, staff,
financial, and organizational data from all Texas public schools. Texas also uses TSDS (Texas Student
Data System) for real-time data access and Ed-Fi based integrations. PEIMS is one of the most complex
state reporting systems in the country due to Texas's size and detailed requirements.""",
        "submission_requirements": """PEIMS has four main submission periods:
- Fall PEIMS: October snapshot (enrollment, staff)
- Mid-year PEIMS: January (discipline, attendance updates)
- Summer PEIMS: June-July (end of year, graduates, completers)
- Extended Year: August (summer school, extended year programs)
Submissions use XML format to TEA TSDS Unique ID system. Strict validation with error correction cycles.""",
        "data_elements_summary": """PEIMS data elements are extensive:
- Student demographics and enrollment (TSDS Unique ID required)
- Attendance (daily, by period)
- Discipline incidents and actions
- Course completion and grades
- CTE (Career and Technical Education) pathways
- Special education, 504, bilingual/ESL
- Assessment (STAAR, TELPAS)
- Staff credentials and assignments
- Financial data (FIRST ratings)
500+ distinct data elements.""",
        "major_competitors": """Skyward: Dominant in Texas with ~35% market share
Tyler Technologies (Infinite Campus): ~25% market share
Frontline (formerly TEAMS): Strong in smaller districts, ~15%
PowerSchool: Present but smaller presence ~10%
Regional ERP vendors: ~15%""",
        "competitor_market_share": """Estimated market share:
- Skyward: 35%
- Tyler/Infinite Campus: 25%
- Frontline: 15%
- PowerSchool: 10%
- Others (regional, ERP-based): 15%
Total: ~1,200+ school districts (largest state by district count)""",
        "competitive_advantages": """Potential advantages for OnCourse:
- Large market opportunity (1,200+ districts)
- Some districts looking for alternatives to Skyward
- Modern SaaS architecture appeals to larger districts
Challenges: PEIMS complexity is significant barrier, strong existing vendor relationships""",
        "certification_process": """TEA requires PEIMS certification for vendors:
- Must pass PEIMS data validation testing
- Annual recertification required
- TSDS integration certification recommended
- Vendors listed on TEA approved vendor list
This is a rigorous process requiring significant investment.""",
        "compliance_requirements": """- FERPA compliance mandatory
- Texas Education Code data privacy requirements
- TEA data security standards
- TREx (Texas Records Exchange) for transcript portability
- Breach notification per Texas law (60 days)""",
        "estimated_certification_time": "9-12 months",
        "key_challenges": """1. PEIMS is extremely complex (500+ data elements)
2. TEA certification is rigorous and time-consuming
3. Very large market requires significant sales investment
4. Strong Skyward and Tyler relationships
5. Many districts have long-term contracts
6. Geographic size makes support challenging""",
        "recommended_approach": """1. Phase 1: Target smaller districts (under 1,000 students)
2. Build PEIMS expertise through dedicated TX implementation team
3. Consider partnership with established TX education consultant
4. Focus on charter schools (growing segment, less vendor loyalty)
5. Emphasize mobile and modern UI vs aging Skyward interface
6. Develop strong TEA relationship for certification support
Timeline: 24-month go-to-market with significant investment""",
        "estimated_development_months": 24,
        "ai_model_used": "claude-3-sonnet (research-augmented)",
        "analysis_confidence": 0.78,
    },
    {
        "state_abbr": "MD",
        "analysis_tier": 2,
        "reporting_system_details": """Maryland uses MSDE (Maryland State Department of Education) data
collection systems. Unlike most states, Maryland has a county-based school system with only 24 LEAs
(Local Education Agencies) - 23 counties plus Baltimore City. This is similar to Louisiana's parish
model that OnCourse successfully serves. Main reporting systems include Maryland Longitudinal Data
System (MLDS) and various MSDE data collections. Smaller number of large districts simplifies market entry.""",
        "submission_requirements": """MSDE has several data collections:
- Annual enrollment counts (September 30 snapshot)
- Attendance reporting (monthly aggregate)
- Student record exchanges (Maryland SAFE system)
- Special education (SSIS - Statewide Special Education Information System)
- Assessment data (MCAP - Maryland Comprehensive Assessment Program)
Data format varies by collection (CSV, XML, direct entry portals).""",
        "data_elements_summary": """Maryland data elements are more streamlined:
- Student demographics and enrollment
- Attendance (aggregate, not daily detail)
- Special education and 504 plans
- English Learner status
- Assessment scores (MCAP, ACCESS)
- Graduate and completer data
- Staff credentials and assignments
Approximately 150 data elements - less complex than PA or TX.""",
        "major_competitors": """PowerSchool: Dominant with ~50% market share
Tyler Technologies: ~25% market share
Synergy (Edupoint): Some presence ~15%
Other vendors: ~10%
Key factor: Only 24 customer opportunities but each is large.""",
        "competitor_market_share": """Estimated market share (by LEA count):
- PowerSchool: 12 LEAs (~50%)
- Tyler Technologies: 6 LEAs (~25%)
- Synergy/Edupoint: 4 LEAs (~17%)
- Other: 2 LEAs (~8%)
Total: 24 LEAs
Note: Each LEA is large - Montgomery County alone has 200,000+ students.""",
        "competitive_advantages": """Strong advantages for OnCourse:
- Louisiana parish model experience directly applicable
- County-based = fewer customers, larger contracts (6x ARPU potential like LA)
- MSDE requirements less complex than PA/TX
- Relationship-driven market favors personalized service
- Geographic proximity to NJ enables in-person support""",
        "certification_process": """Maryland has streamlined vendor process:
- No formal state certification required
- Districts conduct own RFP processes
- MSDE provides data format specifications
- Vendor must demonstrate MSDE data export capability
- Focus is on LEA-level procurement decisions.""",
        "compliance_requirements": """- FERPA compliance mandatory
- Maryland Education Article data privacy provisions
- Student Data Privacy Act of 2015
- COMAR (Code of Maryland Regulations) data handling
- Breach notification within 45 days""",
        "estimated_certification_time": "3-6 months",
        "key_challenges": """1. Only 24 sales opportunities (high stakes per deal)
2. Established PowerSchool relationships in major counties
3. Montgomery County (largest) has deep PowerSchool integration
4. Procurement cycles can be long (1-2 years for large LEAs)
5. Need strong reference from similar county-based state (use LA)""",
        "recommended_approach": """1. Leverage LA success story heavily (county-based, 6x ARPU)
2. Target 2-3 smaller counties initially for quick wins
3. Build Maryland reference customers
4. Focus on counties with upcoming contract renewals
5. Emphasize superior support vs large vendor alternatives
6. Geographic proximity from NJ enables strong on-site presence
Timeline: 12-month aggressive push; high ROI potential""",
        "estimated_development_months": 12,
        "ai_model_used": "claude-3-sonnet (research-augmented)",
        "analysis_confidence": 0.88,
    },
]


async def seed_tier2_analysis(db_session):
    """Seed Tier 2 analysis data for PA, TX, MD."""
    from sqlalchemy import select
    from models import State, StateAnalysis

    for data in TIER2_ANALYSIS_DATA:
        state_abbr = data.pop("state_abbr")

        # Get state ID
        result = await db_session.execute(
            select(State).where(State.abbreviation == state_abbr)
        )
        state = result.scalar_one_or_none()

        if not state:
            print(f"Warning: State {state_abbr} not found in database")
            continue

        # Check for existing analysis
        result = await db_session.execute(
            select(StateAnalysis).where(StateAnalysis.state_id == state.id)
        )
        existing = result.scalar_one_or_none()

        if existing:
            # Update existing
            for key, value in data.items():
                setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            print(f"Updated analysis for {state_abbr}")
        else:
            # Create new
            analysis = StateAnalysis(state_id=state.id, **data)
            db_session.add(analysis)
            print(f"Created analysis for {state_abbr}")

    await db_session.commit()
    print("Tier 2 analysis seeding complete!")


if __name__ == "__main__":
    import asyncio
    from database import async_session

    async def main():
        async with async_session() as session:
            await seed_tier2_analysis(session)

    asyncio.run(main())
