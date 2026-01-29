"""
Baseline capabilities for currently supported states (NJ and LA).

These baselines are used to compare against target states for:
- Technical fit scoring
- Development effort estimation
- Gap analysis

Based on OnCourse Systems' existing implementations.
"""

# New Jersey (NJ) Capabilities
# NJ State Reporting System: NJSMART (NJ Standards Measurement and Resource for Teaching)
NJ_CAPABILITIES = {
    "state": "New Jersey",
    "abbreviation": "NJ",
    "system_name": "NJSMART",
    "doe_url": "https://www.nj.gov/education/",

    # Key features supported
    "key_features": [
        "Student demographics reporting",
        "Staff/teacher certification tracking",
        "Course and grade reporting",
        "Attendance tracking",
        "Discipline incident reporting",
        "Special education (IEP) data",
        "English Language Learner tracking",
        "Assessment data integration",
        "Graduation pathway tracking",
        "Post-secondary enrollment tracking",
    ],

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

    # Data elements count (approximate)
    "data_element_count": 350,

    # Validation complexity
    "validation_rules": {
        "count": 500,
        "complexity": "High",
        "cross_validation": True,
        "real_time_validation": True,
    },

    # Years in production
    "years_supported": 15,

    # District structure
    "district_count": 599,
    "district_model": "Fragmented (individual districts)",

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

    # Key features supported
    "key_features": [
        "Student demographics reporting",
        "Staff certification and credentials",
        "Course enrollment and grades",
        "Attendance and truancy tracking",
        "Discipline reporting (FINS)",
        "Special education services",
        "English Language Learner (ELL) tracking",
        "Assessment data (LEAP, EOC)",
        "Career and Technical Education (CTE)",
        "Early childhood program tracking",
    ],

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

    # Data elements count (approximate)
    "data_element_count": 280,

    # Validation complexity
    "validation_rules": {
        "count": 400,
        "complexity": "Medium-High",
        "cross_validation": True,
        "real_time_validation": True,
    },

    # Years in production
    "years_supported": 8,

    # District structure - KEY DIFFERENTIATOR
    "district_count": 69,
    "district_model": "Parish-based (county model)",

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
            "Parish model = larger contracts",
            "Fewer districts = manageable support",
            "Strong DOE relationship building",
        ],
    },
}


def get_combined_capabilities() -> dict:
    """
    Get combined capabilities from both NJ and LA.

    Useful for determining total feature coverage.
    """
    all_features = set(NJ_CAPABILITIES["key_features"]) | set(LA_CAPABILITIES["key_features"])
    all_formats = set(NJ_CAPABILITIES["submission_formats"]) | set(LA_CAPABILITIES["submission_formats"])

    return {
        "total_features": list(all_features),
        "total_formats": list(all_formats),
        "nj_unique": list(set(NJ_CAPABILITIES["key_features"]) - set(LA_CAPABILITIES["key_features"])),
        "la_unique": list(set(LA_CAPABILITIES["key_features"]) - set(NJ_CAPABILITIES["key_features"])),
        "shared_features": list(set(NJ_CAPABILITIES["key_features"]) & set(LA_CAPABILITIES["key_features"])),
    }


def get_baseline_for_comparison() -> dict:
    """
    Get baselines formatted for AI comparison prompts.
    """
    return {
        "nj": {
            "key_features": NJ_CAPABILITIES["key_features"],
            "data_elements": NJ_CAPABILITIES["data_element_count"],
            "submission_formats": NJ_CAPABILITIES["submission_formats"],
            "district_model": NJ_CAPABILITIES["district_model"],
        },
        "la": {
            "key_features": LA_CAPABILITIES["key_features"],
            "data_elements": LA_CAPABILITIES["data_element_count"],
            "submission_formats": LA_CAPABILITIES["submission_formats"],
            "district_model": LA_CAPABILITIES["district_model"],
        },
    }
