import Link from "next/link";

const rankingFactors = [
  {
    name: "Development Effort",
    weight: 3.0,
    isPrimary: true,
    description:
      "Estimates the development effort required to support a state's reporting requirements. Uses AI analysis of DOE websites and comparison to existing NJ/LA capabilities.",
    scoring: "Lower effort = higher score (inverted). States similar to NJ/LA score higher.",
    dataSource: "AI-powered analysis via Claude API",
  },
  {
    name: "District Structure",
    weight: 2.5,
    isPrimary: false,
    description:
      "Evaluates whether a state uses a county-based model (fewer, larger districts) or a fragmented model (many small districts). County-based models are more favorable.",
    scoring:
      "County-based (like LA parishes, MD counties) scores 8-10. Fragmented (like NJ, TX) scores 1-4.",
    dataSource: "NCES Common Core of Data",
  },
  {
    name: "Average District Size",
    weight: 2.5,
    isPrimary: false,
    description:
      "Calculates the average number of students per district. Larger districts offer higher ARPU (Average Revenue Per User) potential.",
    scoring:
      "30K+ students/district = 9-10. 10-20K = 6-7. Under 2K = 1-2.",
    dataSource: "NCES (total_students / total_districts)",
  },
  {
    name: "Technical Fit",
    weight: 2.0,
    isPrimary: false,
    description:
      "Measures how closely a state's requirements align with existing NJ and LA implementations. Higher overlap means less new development.",
    scoring:
      "Based on data format compatibility, submission workflows, and validation rule similarity.",
    dataSource: "AI-powered comparison via Claude API",
  },
  {
    name: "Certification Complexity",
    weight: 1.5,
    isPrimary: false,
    description:
      "Assesses whether a state requires formal vendor certification or operates an open market. Open markets are easier to enter.",
    scoring:
      "Open market = 7-8. Moderate requirements = 5-6. Formal certification = 3-4. Statewide contracts = 1-3.",
    dataSource: "State DOE documentation research",
  },
  {
    name: "Competitive Landscape",
    weight: 1.5,
    isPrimary: false,
    description:
      "Analyzes the density and strength of competing SIS vendors in the state. Less competition = better opportunity.",
    scoring:
      "Few competitors = 7-9. Moderate competition = 4-6. Saturated market = 1-3.",
    dataSource: "AI-powered market analysis via Claude API",
  },
  {
    name: "Market Opportunity",
    weight: 1.5,
    isPrimary: false,
    description:
      "Evaluates the total market size based on student population and number of districts. Larger markets offer more revenue potential.",
    scoring:
      "3M+ students = 9-10. 1-2M = 6-7. Under 200K = 1-2.",
    dataSource: "NCES Common Core of Data",
  },
  {
    name: "Regulatory Complexity",
    weight: 1.0,
    isPrimary: false,
    description:
      "Considers additional state regulations beyond core reporting, such as privacy laws (beyond FERPA) and audit requirements.",
    scoring:
      "Minimal additional regulations = 7-8. Standard = 5-6. Complex (CCPA, etc.) = 3-4.",
    dataSource: "State regulatory research",
  },
  {
    name: "Geographic Proximity",
    weight: 0.5,
    isPrimary: false,
    description:
      "Measures distance from New Jersey (company HQ). Closer states are easier to support with on-site visits and relationship building.",
    scoring:
      "Adjacent to NJ (PA, NY, DE) = 10. Northeast = 8. West Coast = 2. Alaska/Hawaii = 1.",
    dataSource: "Geographic coordinates calculation",
  },
];

export default function MethodologyPage() {
  return (
    <div className="space-y-8 max-w-4xl">
      <Link
        href="/rankings"
        className="text-blue-600 hover:text-blue-800 dark:text-blue-400"
      >
        &larr; Back to Rankings
      </Link>

      <div>
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
          Ranking Methodology
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400 mt-2">
          How states are scored and ranked for expansion viability
        </p>
      </div>

      {/* Overview */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">
          Overview
        </h2>
        <p className="text-blue-800 dark:text-blue-200 text-sm">
          The ranking system evaluates all 50 US states across 9 weighted factors to
          determine expansion viability for OnCourse Systems. Each factor is scored
          on a 0-10 scale, then multiplied by its weight. The total weighted score
          determines the final ranking.
        </p>
      </div>

      {/* LA Success Story */}
      <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-green-900 dark:text-green-100 mb-2">
          Louisiana Success Story
        </h2>
        <p className="text-green-800 dark:text-green-200 text-sm mb-3">
          Our expansion into Louisiana demonstrates the value of this ranking
          approach. Despite the ~3 year development effort, LA delivers{" "}
          <strong>6x the ARPU</strong> compared to New Jersey.
        </p>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-white dark:bg-zinc-800 p-3 rounded">
            <div className="text-green-600 dark:text-green-400 font-bold text-xl">
              69
            </div>
            <div className="text-zinc-600 dark:text-zinc-400">
              Parishes (vs 599 NJ districts)
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 p-3 rounded">
            <div className="text-green-600 dark:text-green-400 font-bold text-xl">
              6x
            </div>
            <div className="text-zinc-600 dark:text-zinc-400">
              ARPU multiplier
            </div>
          </div>
        </div>
      </div>

      {/* Ranking Factors */}
      <div>
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
          Ranking Factors
        </h2>
        <div className="space-y-4">
          {rankingFactors.map((factor) => (
            <div
              key={factor.name}
              className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-zinc-900 dark:text-white">
                    {factor.name}
                  </h3>
                  {factor.isPrimary && (
                    <span className="text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 px-2 py-0.5 rounded">
                      PRIMARY
                    </span>
                  )}
                </div>
                <span className="text-sm bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                  Weight: {factor.weight}
                </span>
              </div>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-3">
                {factor.description}
              </p>
              <div className="grid md:grid-cols-2 gap-3 text-xs">
                <div className="bg-zinc-50 dark:bg-zinc-900 p-2 rounded">
                  <span className="font-medium text-zinc-700 dark:text-zinc-300">
                    Scoring:
                  </span>{" "}
                  <span className="text-zinc-600 dark:text-zinc-400">
                    {factor.scoring}
                  </span>
                </div>
                <div className="bg-zinc-50 dark:bg-zinc-900 p-2 rounded">
                  <span className="font-medium text-zinc-700 dark:text-zinc-300">
                    Data Source:
                  </span>{" "}
                  <span className="text-zinc-600 dark:text-zinc-400">
                    {factor.dataSource}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Score Calculation */}
      <div className="bg-zinc-100 dark:bg-zinc-800 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-3">
          Score Calculation
        </h2>
        <div className="text-sm text-zinc-700 dark:text-zinc-300 space-y-2">
          <p>
            <strong>Total Score</strong> = Sum of (Factor Score × Factor Weight)
          </p>
          <p>
            <strong>Example:</strong> If a state scores 8 on Development Effort
            (weight 3.0) and 6 on District Structure (weight 2.5):
          </p>
          <p className="font-mono bg-white dark:bg-zinc-900 p-2 rounded">
            (8 × 3.0) + (6 × 2.5) = 24 + 15 = 39 points from these two factors
          </p>
        </div>
      </div>

      {/* Data Sources */}
      <div>
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
          Data Sources
        </h2>
        <ul className="space-y-2 text-sm text-zinc-600 dark:text-zinc-400">
          <li className="flex items-start gap-2">
            <span className="text-blue-500">&#8226;</span>
            <span>
              <strong>NCES Common Core of Data</strong> - District counts, school
              counts, student enrollment (2022-2023)
            </span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-500">&#8226;</span>
            <span>
              <strong>State DOE Websites</strong> - Reporting requirements,
              certification processes
            </span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-500">&#8226;</span>
            <span>
              <strong>Claude AI Analysis</strong> - Development effort estimation,
              technical fit comparison, competitive landscape research
            </span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-500">&#8226;</span>
            <span>
              <strong>Internal Baselines</strong> - NJ and LA implementation
              capabilities for comparison
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
}
