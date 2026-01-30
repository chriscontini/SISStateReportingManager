'use client';

interface StateRecommendation {
  state_name: string;
  state_abbreviation: string;
  total_effort_hours: number;
  projected_months: number;
  total_gaps: number;
  critical_gaps: number;
  baseline_state: string;
}

interface ExecutiveSummaryProps {
  recommendations: StateRecommendation[];
  generatedDate?: string;
}

export default function ExecutiveSummary({
  recommendations,
  generatedDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }),
}: ExecutiveSummaryProps) {
  const handlePrint = () => {
    window.print();
  };

  const handleExportCSV = () => {
    const headers = [
      'Rank',
      'State',
      'Abbreviation',
      'Total Effort (hours)',
      'Projected Months',
      'Total Gaps',
      'Critical Gaps',
      'Baseline Used',
    ];

    const rows = recommendations.map((rec, index) => [
      index + 1,
      rec.state_name,
      rec.state_abbreviation,
      rec.total_effort_hours,
      rec.projected_months,
      rec.total_gaps,
      rec.critical_gaps,
      rec.baseline_state,
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `state_expansion_report_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  const topRecommendation = recommendations[0];

  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow print:shadow-none">
      {/* Header with Actions */}
      <div className="px-6 py-4 border-b border-zinc-200 dark:border-zinc-700 flex justify-between items-center print:hidden">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">
          Executive Summary Report
        </h2>
        <div className="flex gap-2">
          <button
            onClick={handleExportCSV}
            className="px-4 py-2 text-sm font-medium text-zinc-700 bg-white border border-zinc-300 rounded-md hover:bg-zinc-50 dark:bg-zinc-700 dark:text-zinc-300 dark:border-zinc-600 dark:hover:bg-zinc-600"
          >
            Export CSV
          </button>
          <button
            onClick={handlePrint}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Print Report
          </button>
        </div>
      </div>

      {/* Report Content */}
      <div className="p-6 print:p-0">
        {/* Report Header */}
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-white">
            SIS State Expansion Analysis
          </h1>
          <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
            Generated: {generatedDate}
          </p>
        </div>

        {/* Top Recommendation */}
        {topRecommendation && (
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-green-900 dark:text-green-100 mb-2">
              Primary Recommendation
            </h3>
            <p className="text-2xl font-bold text-green-800 dark:text-green-200">
              {topRecommendation.state_name} ({topRecommendation.state_abbreviation})
            </p>
            <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <div className="text-sm text-green-700 dark:text-green-300">Effort</div>
                <div className="font-semibold text-green-900 dark:text-green-100">
                  {topRecommendation.total_effort_hours.toLocaleString()} hours
                </div>
              </div>
              <div>
                <div className="text-sm text-green-700 dark:text-green-300">Timeline</div>
                <div className="font-semibold text-green-900 dark:text-green-100">
                  {topRecommendation.projected_months} months
                </div>
              </div>
              <div>
                <div className="text-sm text-green-700 dark:text-green-300">Total Gaps</div>
                <div className="font-semibold text-green-900 dark:text-green-100">
                  {topRecommendation.total_gaps}
                </div>
              </div>
              <div>
                <div className="text-sm text-green-700 dark:text-green-300">Baseline</div>
                <div className="font-semibold text-green-900 dark:text-green-100">
                  {topRecommendation.baseline_state}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* All Recommendations */}
        <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
          State Rankings (by Effort)
        </h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
            <thead>
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Rank
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  State
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Effort (hrs)
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Timeline
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Gaps
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Critical
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Baseline
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
              {recommendations.map((rec, index) => (
                <tr key={rec.state_abbreviation} className={index === 0 ? 'bg-green-50 dark:bg-green-900/10' : ''}>
                  <td className="px-4 py-3 text-sm font-medium text-zinc-900 dark:text-white">
                    #{index + 1}
                  </td>
                  <td className="px-4 py-3 text-sm text-zinc-900 dark:text-white">
                    {rec.state_name} ({rec.state_abbreviation})
                  </td>
                  <td className="px-4 py-3 text-sm text-zinc-900 dark:text-white">
                    {rec.total_effort_hours.toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-sm text-zinc-900 dark:text-white">
                    {rec.projected_months} months
                  </td>
                  <td className="px-4 py-3 text-sm text-zinc-900 dark:text-white">
                    {rec.total_gaps}
                  </td>
                  <td className="px-4 py-3 text-sm">
                    <span className={rec.critical_gaps > 5 ? 'text-red-600 dark:text-red-400' : 'text-zinc-900 dark:text-white'}>
                      {rec.critical_gaps}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-zinc-900 dark:text-white">
                    {rec.baseline_state}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Key Metrics */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
            Key Decision Metrics
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-zinc-50 dark:bg-zinc-900/50 rounded-lg p-4">
              <div className="text-sm text-zinc-500 dark:text-zinc-400">LA Benchmark</div>
              <div className="text-xl font-bold text-zinc-900 dark:text-white">30 months</div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400">15,000 hours / 5 FTE</div>
            </div>
            <div className="bg-zinc-50 dark:bg-zinc-900/50 rounded-lg p-4">
              <div className="text-sm text-zinc-500 dark:text-zinc-400">LA ARPU Increase</div>
              <div className="text-xl font-bold text-zinc-900 dark:text-white">6x</div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400">Parish model advantage</div>
            </div>
            <div className="bg-zinc-50 dark:bg-zinc-900/50 rounded-lg p-4">
              <div className="text-sm text-zinc-500 dark:text-zinc-400">States Analyzed</div>
              <div className="text-xl font-bold text-zinc-900 dark:text-white">{recommendations.length}</div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400">Ranked by effort</div>
            </div>
          </div>
        </div>

        {/* Action Items */}
        <div className="mt-8">
          <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
            Recommended Next Steps
          </h3>
          <ol className="list-decimal list-inside space-y-2 text-sm text-zinc-700 dark:text-zinc-300">
            <li>Review detailed gap analysis for recommended state(s)</li>
            <li>Validate effort estimates with development team leads</li>
            <li>Initiate DOE relationship building for target state</li>
            <li>Conduct detailed requirements gathering sessions</li>
            <li>Create phased implementation roadmap</li>
            <li>Allocate resources and establish project timeline</li>
          </ol>
        </div>

        {/* Footer */}
        <div className="mt-8 pt-4 border-t border-zinc-200 dark:border-zinc-700 text-center text-xs text-zinc-500 dark:text-zinc-400">
          <p>Generated by SIS State Reporting Manager</p>
          <p>OnCourse Systems for Education</p>
        </div>
      </div>
    </div>
  );
}
