"""
Baseline capabilities for currently supported states (NJ and LA).

These baselines are used to compare against target states for:
- Technical fit scoring
- Development effort estimation
- Gap analysis

Based on OnCourse Systems' existing implementations.

Expanded in Sprint 4 with detailed capability mappings for gap analysis.
"""

from typing import Any


# Feature Categories for gap analysis
FEATURE_CATEGORIES = [
    "enrollment",
    "attendance",
    "grades",
    "special_ed",
    "assessments",
    "staff",
    "discipline",
    "ell",
    "cte",
    "reporting",
    "integration",
    "certification",
]


# New Jersey (NJ) Capabilities
# NJ State Reporting System: NJSMART (NJ Standards Measurement and Resource for Teaching)
NJ_CAPABILITIES = {
    "state": "New Jersey",
    "abbreviation": "NJ",
    "system_name": "NJSMART",
    "doe_url": "https://www.nj.gov/education/",

    # District structure
    "district_count": 599,
    "district_model": "Fragmented (individual districts)",

    # Data elements count (approximate)
    "data_element_count": 350,

    # Years in production
    "years_supported": 15,

    # Detailed capabilities by category
    "capabilities": {
        "enrollment": [
            {
                "code": "NJ-ENR-001",
                "name": "Student Demographics",
                "description": "Complete student demographic data including name, DOB, gender, race/ethnicity, address",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "NJ-ENR-002",
                "name": "Student Identification",
                "description": "State student ID (SID) assignment and tracking",
                "complexity": "low",
                "effort_hours": 40,
            },
            {
                "code": "NJ-ENR-003",
                "name": "Enrollment Status Tracking",
                "description": "Entry/exit codes, enrollment dates, withdrawal reasons",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-ENR-004",
                "name": "Grade Level Management",
                "description": "Grade level assignment, retention tracking, promotion",
                "complexity": "low",
                "effort_hours": 30,
            },
            {
                "code": "NJ-ENR-005",
                "name": "District/School Assignment",
                "description": "LEA and school code assignment, transfers between schools",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "NJ-ENR-006",
                "name": "Residency Tracking",
                "description": "Student residency status, sending/receiving district relationships",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "NJ-ENR-007",
                "name": "Homeless Student Tracking",
                "description": "McKinney-Vento homeless status and services",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-ENR-008",
                "name": "Foster Care Status",
                "description": "Foster care enrollment tracking and liaison coordination",
                "complexity": "medium",
                "effort_hours": 50,
            },
        ],
        "attendance": [
            {
                "code": "NJ-ATT-001",
                "name": "Daily Attendance",
                "description": "Daily attendance tracking with absence codes",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "NJ-ATT-002",
                "name": "Period Attendance",
                "description": "Period-by-period attendance for secondary schools",
                "complexity": "high",
                "effort_hours": 120,
            },
            {
                "code": "NJ-ATT-003",
                "name": "Chronic Absenteeism",
                "description": "Chronic absenteeism calculation and reporting",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-ATT-004",
                "name": "Truancy Tracking",
                "description": "Truancy petition tracking and intervention documentation",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "NJ-ATT-005",
                "name": "Excused/Unexcused Classification",
                "description": "NJ-specific absence code mapping and validation",
                "complexity": "low",
                "effort_hours": 40,
            },
        ],
        "grades": [
            {
                "code": "NJ-GRD-001",
                "name": "Course Enrollment",
                "description": "Course section assignment and scheduling",
                "complexity": "high",
                "effort_hours": 120,
            },
            {
                "code": "NJ-GRD-002",
                "name": "Grade Recording",
                "description": "Marking period and final grade recording",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "NJ-GRD-003",
                "name": "GPA Calculation",
                "description": "Weighted and unweighted GPA calculation",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-GRD-004",
                "name": "Credit Accumulation",
                "description": "Credit earned tracking for graduation requirements",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "NJ-GRD-005",
                "name": "SCED Course Codes",
                "description": "SCED (School Codes for the Exchange of Data) mapping",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "NJ-GRD-006",
                "name": "Dual Enrollment",
                "description": "College course enrollment and credit tracking",
                "complexity": "high",
                "effort_hours": 100,
            },
        ],
        "special_ed": [
            {
                "code": "NJ-SPED-001",
                "name": "IEP Management",
                "description": "Individualized Education Program tracking and dates",
                "complexity": "high",
                "effort_hours": 150,
            },
            {
                "code": "NJ-SPED-002",
                "name": "Disability Categories",
                "description": "Primary and secondary disability code assignment",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-SPED-003",
                "name": "Placement Settings",
                "description": "Educational environment/placement setting tracking",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "NJ-SPED-004",
                "name": "Related Services",
                "description": "Related services tracking (speech, OT, PT, counseling)",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "NJ-SPED-005",
                "name": "Exit Reasons",
                "description": "Special education exit reason codes and transitions",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "NJ-SPED-006",
                "name": "504 Plans",
                "description": "Section 504 accommodation plan tracking",
                "complexity": "medium",
                "effort_hours": 60,
            },
        ],
        "assessments": [
            {
                "code": "NJ-ASM-001",
                "name": "NJSLA Integration",
                "description": "NJ Student Learning Assessment data import/export",
                "complexity": "high",
                "effort_hours": 120,
            },
            {
                "code": "NJ-ASM-002",
                "name": "Assessment Registration",
                "description": "State assessment student registration files",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "NJ-ASM-003",
                "name": "Assessment Accommodations",
                "description": "Testing accommodation assignment and tracking",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "NJ-ASM-004",
                "name": "Score Import",
                "description": "Assessment score import and student matching",
                "complexity": "high",
                "effort_hours": 90,
            },
            {
                "code": "NJ-ASM-005",
                "name": "Alternate Assessments",
                "description": "Dynamic Learning Maps (DLM) for students with significant cognitive disabilities",
                "complexity": "high",
                "effort_hours": 80,
            },
        ],
        "staff": [
            {
                "code": "NJ-STF-001",
                "name": "Staff Demographics",
                "description": "Staff basic information and contact details",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-STF-002",
                "name": "Certification Tracking",
                "description": "NJ teaching certificate/license tracking",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "NJ-STF-003",
                "name": "Highly Qualified Status",
                "description": "Teacher HQ status tracking by subject",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "NJ-STF-004",
                "name": "Staff Assignment",
                "description": "Staff-to-school and staff-to-class assignments",
                "complexity": "high",
                "effort_hours": 90,
            },
            {
                "code": "NJ-STF-005",
                "name": "Position Codes",
                "description": "NJ position/job classification codes",
                "complexity": "medium",
                "effort_hours": 50,
            },
        ],
        "discipline": [
            {
                "code": "NJ-DIS-001",
                "name": "Incident Recording",
                "description": "Discipline incident documentation",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "NJ-DIS-002",
                "name": "Action Codes",
                "description": "NJ discipline action/consequence codes",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "NJ-DIS-003",
                "name": "HIB Reporting",
                "description": "Harassment, Intimidation, and Bullying incident tracking",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "NJ-DIS-004",
                "name": "Removal Days",
                "description": "In-school and out-of-school suspension day tracking",
                "complexity": "medium",
                "effort_hours": 60,
            },
        ],
        "ell": [
            {
                "code": "NJ-ELL-001",
                "name": "ELL Identification",
                "description": "English Language Learner identification and status",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-ELL-002",
                "name": "Home Language Survey",
                "description": "Home language survey tracking",
                "complexity": "low",
                "effort_hours": 30,
            },
            {
                "code": "NJ-ELL-003",
                "name": "Program Placement",
                "description": "Bilingual/ESL program placement tracking",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-ELL-004",
                "name": "ACCESS Scores",
                "description": "ACCESS for ELLs assessment score tracking",
                "complexity": "high",
                "effort_hours": 80,
            },
            {
                "code": "NJ-ELL-005",
                "name": "Exit Criteria",
                "description": "ELL program exit monitoring and former ELL tracking",
                "complexity": "medium",
                "effort_hours": 50,
            },
        ],
        "cte": [
            {
                "code": "NJ-CTE-001",
                "name": "CTE Program Enrollment",
                "description": "Career and Technical Education program participation",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "NJ-CTE-002",
                "name": "Industry Credentials",
                "description": "Industry certification/credential tracking",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "NJ-CTE-003",
                "name": "CIP Codes",
                "description": "Classification of Instructional Programs code assignment",
                "complexity": "medium",
                "effort_hours": 50,
            },
        ],
        "reporting": [
            {
                "code": "NJ-RPT-001",
                "name": "NJSMART Submission",
                "description": "Core NJSMART file generation and submission",
                "complexity": "very_high",
                "effort_hours": 200,
            },
            {
                "code": "NJ-RPT-002",
                "name": "Fall Submission",
                "description": "October fall enrollment snapshot reporting",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "NJ-RPT-003",
                "name": "End of Year Submission",
                "description": "EOY comprehensive data submission",
                "complexity": "very_high",
                "effort_hours": 150,
            },
            {
                "code": "NJ-RPT-004",
                "name": "Validation Error Resolution",
                "description": "NJSMART validation error handling and correction workflow",
                "complexity": "high",
                "effort_hours": 120,
            },
            {
                "code": "NJ-RPT-005",
                "name": "District Verification",
                "description": "District data verification and sign-off process",
                "complexity": "medium",
                "effort_hours": 60,
            },
        ],
        "integration": [
            {
                "code": "NJ-INT-001",
                "name": "NJSMART Portal Integration",
                "description": "Direct integration with NJSMART web portal",
                "complexity": "high",
                "effort_hours": 150,
            },
            {
                "code": "NJ-INT-002",
                "name": "School Performance Reports",
                "description": "Data feed for NJ School Performance Reports",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "NJ-INT-003",
                "name": "PARCC/NJSLA Data Exchange",
                "description": "Assessment data bidirectional exchange",
                "complexity": "high",
                "effort_hours": 120,
            },
        ],
        "certification": [
            {
                "code": "NJ-CERT-001",
                "name": "State Approval",
                "description": "NJ DOE approval/certification process completion",
                "complexity": "high",
                "effort_hours": 200,
            },
        ],
    },

    # Submission formats supported
    "submission_formats": [
        "XML file upload",
        "CSV file upload",
        "Web portal entry",
        "API integration (limited)",
    ],

    # Reporting calendar
    "reporting_periods": [
        "Fall submission (October)",
        "End of Year submission (June/July)",
        "Assessment windows (varies)",
    ],

    # Validation complexity
    "validation_rules": {
        "count": 500,
        "complexity": "High",
        "cross_validation": True,
        "real_time_validation": True,
    },

    # Integration notes
    "integration_notes": [
        "NJ Student Learning Assessment (NJSLA) integration",
        "PARCC transition handled",
        "School Performance Reports data",
        "Multiple LEA types (traditional, charter, renaissance)",
    ],
}


# Louisiana (LA) Capabilities
# LA State Reporting System: SIS State Reporting / EdLink
LA_CAPABILITIES = {
    "state": "Louisiana",
    "abbreviation": "LA",
    "system_name": "EdLink / SIS State Reporting",
    "doe_url": "https://www.louisianabelieves.com/",

    # District structure - KEY DIFFERENTIATOR
    "district_count": 69,
    "district_model": "Parish-based (county model)",

    # Data elements count (approximate)
    "data_element_count": 280,

    # Years in production
    "years_supported": 8,

    # Detailed capabilities by category
    "capabilities": {
        "enrollment": [
            {
                "code": "LA-ENR-001",
                "name": "Student Demographics",
                "description": "Complete student demographic data per Louisiana requirements",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "LA-ENR-002",
                "name": "State Student ID",
                "description": "Louisiana SID assignment via EdLink",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-ENR-003",
                "name": "Enrollment Tracking",
                "description": "Entry/exit codes, enrollment dates with LA-specific codes",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-ENR-004",
                "name": "Grade Level",
                "description": "Grade level assignment including early childhood grades",
                "complexity": "low",
                "effort_hours": 40,
            },
            {
                "code": "LA-ENR-005",
                "name": "Parish/School Assignment",
                "description": "Parish-based LEA and school site assignment",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "LA-ENR-006",
                "name": "Residency",
                "description": "Student residency and tuition status",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-ENR-007",
                "name": "Homeless Status",
                "description": "McKinney-Vento homeless student tracking",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "LA-ENR-008",
                "name": "Foster Care",
                "description": "Foster care student identification",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "LA-ENR-009",
                "name": "Early Childhood Enrollment",
                "description": "Pre-K and LA-4 program enrollment tracking",
                "complexity": "high",
                "effort_hours": 100,
            },
        ],
        "attendance": [
            {
                "code": "LA-ATT-001",
                "name": "Daily Attendance",
                "description": "Daily attendance with LA absence codes",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "LA-ATT-002",
                "name": "Period Attendance",
                "description": "Period-by-period attendance tracking",
                "complexity": "high",
                "effort_hours": 110,
            },
            {
                "code": "LA-ATT-003",
                "name": "Chronic Absenteeism",
                "description": "Chronic absenteeism tracking for accountability",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-ATT-004",
                "name": "Truancy/FINS",
                "description": "Families in Need of Services referral tracking",
                "complexity": "high",
                "effort_hours": 90,
            },
            {
                "code": "LA-ATT-005",
                "name": "Membership Days",
                "description": "Student membership days calculation for MFP",
                "complexity": "high",
                "effort_hours": 100,
            },
        ],
        "grades": [
            {
                "code": "LA-GRD-001",
                "name": "Course Enrollment",
                "description": "Course section assignment and master schedule",
                "complexity": "high",
                "effort_hours": 120,
            },
            {
                "code": "LA-GRD-002",
                "name": "Grade Recording",
                "description": "Marking period and final grades",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "LA-GRD-003",
                "name": "GPA Calculation",
                "description": "Louisiana GPA calculation with TOPS scale",
                "complexity": "high",
                "effort_hours": 80,
            },
            {
                "code": "LA-GRD-004",
                "name": "Carnegie Units",
                "description": "Carnegie unit tracking for graduation",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-GRD-005",
                "name": "SCED Codes",
                "description": "SCED course code mapping for state reporting",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "LA-GRD-006",
                "name": "Dual Enrollment",
                "description": "Dual enrollment course tracking",
                "complexity": "high",
                "effort_hours": 90,
            },
            {
                "code": "LA-GRD-007",
                "name": "TOPS Core Curriculum",
                "description": "TOPS core curriculum completion tracking",
                "complexity": "high",
                "effort_hours": 100,
            },
        ],
        "special_ed": [
            {
                "code": "LA-SPED-001",
                "name": "IEP Management",
                "description": "IEP tracking and date management",
                "complexity": "high",
                "effort_hours": 150,
            },
            {
                "code": "LA-SPED-002",
                "name": "Exceptionality Codes",
                "description": "Louisiana exceptionality/disability codes",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-SPED-003",
                "name": "Placement/LRE",
                "description": "Educational environment tracking",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "LA-SPED-004",
                "name": "Related Services",
                "description": "Related services documentation",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "LA-SPED-005",
                "name": "Transition Services",
                "description": "Post-secondary transition planning",
                "complexity": "high",
                "effort_hours": 80,
            },
            {
                "code": "LA-SPED-006",
                "name": "Gifted/Talented",
                "description": "Gifted and talented student tracking",
                "complexity": "medium",
                "effort_hours": 60,
            },
        ],
        "assessments": [
            {
                "code": "LA-ASM-001",
                "name": "LEAP 2025",
                "description": "LEAP 2025 assessment data integration",
                "complexity": "high",
                "effort_hours": 120,
            },
            {
                "code": "LA-ASM-002",
                "name": "EOC Exams",
                "description": "End-of-Course exam tracking",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "LA-ASM-003",
                "name": "Assessment Registration",
                "description": "State assessment student registration",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "LA-ASM-004",
                "name": "Accommodations",
                "description": "Testing accommodation management",
                "complexity": "high",
                "effort_hours": 90,
            },
            {
                "code": "LA-ASM-005",
                "name": "LAA1/LEAP Connect",
                "description": "Alternate assessment for significant disabilities",
                "complexity": "high",
                "effort_hours": 80,
            },
            {
                "code": "LA-ASM-006",
                "name": "ACT/WorkKeys",
                "description": "ACT and WorkKeys score import",
                "complexity": "medium",
                "effort_hours": 60,
            },
        ],
        "staff": [
            {
                "code": "LA-STF-001",
                "name": "Staff Demographics",
                "description": "Staff demographic information",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-STF-002",
                "name": "Certification",
                "description": "LA teaching certificate tracking via TEACH system",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "LA-STF-003",
                "name": "Staff Assignment",
                "description": "Staff-to-course and staff-to-school assignments",
                "complexity": "high",
                "effort_hours": 90,
            },
            {
                "code": "LA-STF-004",
                "name": "VAM/Compass",
                "description": "Value-Added Model/Compass evaluation data",
                "complexity": "high",
                "effort_hours": 120,
            },
        ],
        "discipline": [
            {
                "code": "LA-DIS-001",
                "name": "Incident Recording",
                "description": "Discipline incident documentation",
                "complexity": "medium",
                "effort_hours": 80,
            },
            {
                "code": "LA-DIS-002",
                "name": "LA Action Codes",
                "description": "Louisiana-specific discipline action codes",
                "complexity": "medium",
                "effort_hours": 50,
            },
            {
                "code": "LA-DIS-003",
                "name": "Bullying/Cyberbullying",
                "description": "Bullying and cyberbullying incident tracking",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "LA-DIS-004",
                "name": "FINS Referrals",
                "description": "Families in Need of Services discipline referrals",
                "complexity": "high",
                "effort_hours": 90,
            },
        ],
        "ell": [
            {
                "code": "LA-ELL-001",
                "name": "EL Identification",
                "description": "English Learner identification and HLS",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-ELL-002",
                "name": "EL Program",
                "description": "EL program placement and services",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-ELL-003",
                "name": "ELPT Scores",
                "description": "English Language Proficiency Test score tracking",
                "complexity": "high",
                "effort_hours": 80,
            },
            {
                "code": "LA-ELL-004",
                "name": "EL Exit/Monitoring",
                "description": "EL exit and monitoring year tracking",
                "complexity": "medium",
                "effort_hours": 50,
            },
        ],
        "cte": [
            {
                "code": "LA-CTE-001",
                "name": "Jump Start Pathways",
                "description": "Jump Start career pathway enrollment",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "LA-CTE-002",
                "name": "Industry Credentials",
                "description": "Industry-Based Credential tracking (IBC)",
                "complexity": "high",
                "effort_hours": 90,
            },
            {
                "code": "LA-CTE-003",
                "name": "CTE Concentrator",
                "description": "CTE concentrator status tracking",
                "complexity": "medium",
                "effort_hours": 60,
            },
            {
                "code": "LA-CTE-004",
                "name": "Work-Based Learning",
                "description": "Work-based learning hours and experiences",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "LA-CTE-005",
                "name": "TOPS Tech",
                "description": "TOPS Tech diploma pathway tracking",
                "complexity": "high",
                "effort_hours": 80,
            },
        ],
        "early_childhood": [
            {
                "code": "LA-EC-001",
                "name": "CLASS Observations",
                "description": "CLASS assessment observation data",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "LA-EC-002",
                "name": "Pre-K Program Types",
                "description": "LA-4, NSECD, Head Start program tracking",
                "complexity": "medium",
                "effort_hours": 70,
            },
            {
                "code": "LA-EC-003",
                "name": "Kindergarten Readiness",
                "description": "Kindergarten readiness assessment data",
                "complexity": "medium",
                "effort_hours": 60,
            },
        ],
        "reporting": [
            {
                "code": "LA-RPT-001",
                "name": "SIS Submission",
                "description": "Core SIS file generation for EdLink",
                "complexity": "very_high",
                "effort_hours": 200,
            },
            {
                "code": "LA-RPT-002",
                "name": "October 1 Count",
                "description": "October enrollment count reporting",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "LA-RPT-003",
                "name": "February 1 Count",
                "description": "February enrollment count reporting",
                "complexity": "high",
                "effort_hours": 80,
            },
            {
                "code": "LA-RPT-004",
                "name": "End of Year",
                "description": "End of year comprehensive submission",
                "complexity": "very_high",
                "effort_hours": 150,
            },
            {
                "code": "LA-RPT-005",
                "name": "Validation Resolution",
                "description": "EdLink validation error resolution workflow",
                "complexity": "high",
                "effort_hours": 120,
            },
        ],
        "integration": [
            {
                "code": "LA-INT-001",
                "name": "EdLink Portal",
                "description": "EdLink web portal integration",
                "complexity": "high",
                "effort_hours": 150,
            },
            {
                "code": "LA-INT-002",
                "name": "SIF Agent",
                "description": "Schools Interoperability Framework agent",
                "complexity": "very_high",
                "effort_hours": 200,
            },
            {
                "code": "LA-INT-003",
                "name": "School Performance",
                "description": "School Performance Score data feed",
                "complexity": "high",
                "effort_hours": 100,
            },
            {
                "code": "LA-INT-004",
                "name": "TEACH Integration",
                "description": "TEACH certification system integration",
                "complexity": "high",
                "effort_hours": 120,
            },
        ],
        "certification": [
            {
                "code": "LA-CERT-001",
                "name": "State Approval",
                "description": "LDOE approval and certification process",
                "complexity": "high",
                "effort_hours": 180,
            },
        ],
    },

    # Submission formats supported
    "submission_formats": [
        "SIF (Schools Interoperability Framework)",
        "CSV file upload",
        "EdLink portal",
        "API integration",
    ],

    # Reporting calendar
    "reporting_periods": [
        "October 1 count",
        "February 1 count",
        "End of Year (July)",
        "Periodic uploads throughout year",
    ],

    # Validation complexity
    "validation_rules": {
        "count": 400,
        "complexity": "Medium-High",
        "cross_validation": True,
        "real_time_validation": True,
    },

    # Integration notes
    "integration_notes": [
        "Parish model allows for larger district relationships",
        "Unified accountability system integration",
        "Jump Start (CTE) credential tracking",
        "Early childhood (CLASS) assessments",
        "School and center performance score integration",
    ],

    # LA Expansion success story
    "expansion_metrics": {
        "time_to_market": "2.5-3 years",
        "arpu_multiplier": 6.0,  # 6x ARPU compared to NJ
        "district_adoption_rate": "Moderate",
        "key_success_factors": [
            "Parish model = larger contracts (avg 10k students vs 1.5k in NJ)",
            "Fewer districts = manageable support load (69 vs 599)",
            "Strong DOE relationship building",
            "SIF framework reduced integration complexity",
            "Early childhood focus aligned with state priorities",
            "Jump Start CTE differentiator",
        ],
        "total_development_hours": 15000,
        "total_months": 30,
        "team_size_fte": 5,
    },
}


def get_capability_count(baseline: dict) -> dict:
    """Get count of capabilities by category for a baseline."""
    counts = {}
    total = 0
    for category, capabilities in baseline.get("capabilities", {}).items():
        counts[category] = len(capabilities)
        total += len(capabilities)
    counts["total"] = total
    return counts


def get_total_effort_hours(baseline: dict) -> int:
    """Calculate total effort hours for all capabilities in a baseline."""
    total = 0
    for category, capabilities in baseline.get("capabilities", {}).items():
        for cap in capabilities:
            total += cap.get("effort_hours", 0)
    return total


def get_capabilities_by_category(baseline: dict, category: str) -> list:
    """Get all capabilities for a specific category."""
    return baseline.get("capabilities", {}).get(category, [])


def get_combined_capabilities() -> dict:
    """
    Get combined capabilities from both NJ and LA.

    Useful for determining total feature coverage.
    """
    nj_features = []
    la_features = []

    for caps in NJ_CAPABILITIES.get("capabilities", {}).values():
        nj_features.extend([c["name"] for c in caps])

    for caps in LA_CAPABILITIES.get("capabilities", {}).values():
        la_features.extend([c["name"] for c in caps])

    all_features = set(nj_features) | set(la_features)

    return {
        "total_features": list(all_features),
        "total_formats": list(set(NJ_CAPABILITIES["submission_formats"]) | set(LA_CAPABILITIES["submission_formats"])),
        "nj_unique": list(set(nj_features) - set(la_features)),
        "la_unique": list(set(la_features) - set(nj_features)),
        "shared_features": list(set(nj_features) & set(la_features)),
        "nj_count": get_capability_count(NJ_CAPABILITIES),
        "la_count": get_capability_count(LA_CAPABILITIES),
        "nj_effort_hours": get_total_effort_hours(NJ_CAPABILITIES),
        "la_effort_hours": get_total_effort_hours(LA_CAPABILITIES),
    }


def get_baseline_for_comparison() -> dict:
    """
    Get baselines formatted for AI comparison prompts.
    """
    return {
        "nj": {
            "capabilities": NJ_CAPABILITIES.get("capabilities", {}),
            "data_elements": NJ_CAPABILITIES["data_element_count"],
            "submission_formats": NJ_CAPABILITIES["submission_formats"],
            "district_model": NJ_CAPABILITIES["district_model"],
            "district_count": NJ_CAPABILITIES["district_count"],
            "years_supported": NJ_CAPABILITIES["years_supported"],
        },
        "la": {
            "capabilities": LA_CAPABILITIES.get("capabilities", {}),
            "data_elements": LA_CAPABILITIES["data_element_count"],
            "submission_formats": LA_CAPABILITIES["submission_formats"],
            "district_model": LA_CAPABILITIES["district_model"],
            "district_count": LA_CAPABILITIES["district_count"],
            "years_supported": LA_CAPABILITIES["years_supported"],
            "expansion_metrics": LA_CAPABILITIES["expansion_metrics"],
        },
    }


def find_matching_capability(
    baseline: dict,
    target_name: str,
    category: str | None = None
) -> dict | None:
    """
    Find a capability in a baseline that matches a target name.

    Returns the matching capability dict or None if not found.
    """
    categories_to_search = (
        [category] if category else list(baseline.get("capabilities", {}).keys())
    )

    target_lower = target_name.lower()

    for cat in categories_to_search:
        for cap in baseline.get("capabilities", {}).get(cat, []):
            if target_lower in cap["name"].lower():
                return cap
    return None


def estimate_effort_from_la_benchmark(capability_count: int) -> dict:
    """
    Estimate effort based on LA expansion benchmark.

    LA took 30 months with ~60 capabilities. Use this ratio for estimates.
    """
    la_metrics = LA_CAPABILITIES["expansion_metrics"]
    la_capability_count = get_capability_count(LA_CAPABILITIES)["total"]

    # Calculate ratio
    ratio = capability_count / la_capability_count

    return {
        "estimated_months": round(la_metrics["total_months"] * ratio),
        "estimated_hours": round(la_metrics["total_development_hours"] * ratio),
        "estimated_fte": round(la_metrics["team_size_fte"] * ratio, 1),
        "benchmark_note": f"Based on LA expansion: {la_metrics['total_months']} months, {la_capability_count} capabilities",
    }
